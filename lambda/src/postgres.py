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


def upsert_moodnotes(args_list):
    conn = get_conn()
    cur = conn.cursor()
    args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s)", tpl).decode('utf-8') for tpl in args_list)
    cur.execute("""
                INSERT INTO public.moodnotes(
                    id, mood_value, incident, page_created, page_updated)
                VALUES
                """ + args_str + " ON CONFLICT (id ,page_created) DO NOTHING")
                # 本来は ON CONFLITでUPDATEした方がいいのだが、そこまで考えて設計してなかった(*´∀｀*)
    conn.commit()
    conn.close()

def upsert_spent_time(id, location, date, spent_time):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
            INSERT INTO public.spent_time(
            id, location, date, spent_time)
            VALUES ((%s), (%s), (%s), (%s))
            ON CONFLICT (id, location, date) DO UPDATE SET spent_time = (%s);
        """, (id, location, date, spent_time, spent_time)
    )
    conn.commit()
    conn.close()
