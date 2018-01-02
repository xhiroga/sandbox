import os
import psycopg2
import urllib.parse
import requests
from datetime import date
from datetime import datetime as dt
from datetime import timedelta
import pytz


def get_conn():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["METADATA_POSTGRES_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn


def get_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
            SELECT
                userid
            FROM
                step_count_config.user
            WHERE
                delete_timestamp = 'infinity';
        """
    )
    # 0件なら空リストが返る
    return cur.fetchall()


def get_repos(userid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
            SELECT
                repo_owner,
                repo_name
            FROM
                step_count_config.watch_repositories
            WHERE
                delete_timestamp = 'infinity';
        """
    )
    # 0件なら空リストが返る
    return cur.fetchall()


def insert_total_count(day, userid, total_count):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
            INSERT INTO public.pgm_step_count(
                create_timestamp, update_timestamp, delete_timestamp,
                user_id, date, count)
            VALUES ('NOW', 'NOW', 'INFINITY', (%s), (%s), (%s))
            ON CONFLICT (user_id, date) DO UPDATE SET count = (%s);
        """, (userid, day, total_count, total_count)
    )
    conn.commit()
    conn.close()


def get_addition_count(day, userid, repos):
    ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
    LIST_COMMITS_API = "https://api.github.com/repos/{0}/{1}/commits?since='{2}'"
    SINGLE_COMMIT_API = "https://api.github.com/repos/{0}/{1}/commits/{2}"

    total_count = 0

    t = dt.strptime(day, '%Y-%m-%d')
    dt_jst = pytz.timezone("Asia/Tokyo").localize(t)
    dt_utc = dt_jst.astimezone(pytz.utc)

    for rp in repos:
        commits = requests.get(LIST_COMMITS_API.format(rp[0], rp[1], dt.strftime(dt_utc, ISO8601))).json()
        # パラメータを複数指定することで対象commitを絞り込むこともできるのだが、そうするとresponseがなんか変になる...

        for cmt in commits:
            cmt_datetime = pytz.timezone('UTC').localize(dt.strptime(cmt["commit"]["author"]["date"], ISO8601))
            if dt_utc <= cmt_datetime and cmt_datetime <= dt_utc + timedelta(days=1) and cmt["author"]["login"] == userid:
                commit = requests.get(SINGLE_COMMIT_API.format(rp[0],rp[1],cmt["sha"])).json()
                total_count += commit["stats"]["additions"]
    return total_count


# day expects "YYYY-MM-DD"
def add_step_count(day):
    for userid in get_users():
        repos = get_repos(userid)
        total_count = get_addition_count(day, userid, repos)
        insert_total_count(day, userid, total_count)
    print("OK")


add_step_count(dt.strftime(date.today(), '%Y-%m-%d'))
