import os
import psycopg2
import urllib.parse


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
