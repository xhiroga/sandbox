from datetime import date
from datetime import datetime as dt
from datetime import timedelta
import logging
import sys
sys.path.insert(0, "../common/")
import pandas as pd
import postgres as pg
import pytz
import add_step_count as add


def range_handler(start, end):

    mylog = logging.getLogger("mylog")
    mylog.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(fmt)
    mylog.addHandler(ch)

    for userid in pg.get_users():
        userid = userid[0]
        # userid type = tuple, レコードの一行の列が格納されている建前のため
        mylog.debug("userid:" + userid)

        for day in pd.date_range(start, end):
            mylog.debug("day: " + day.strftime("%Y-%m-%d"))

            repos = pg.get_repos(userid)
            mylog.debug(repos)

            total_count = add.get_addition_count(pytz.timezone('Asia/Tokyo').localize(day).astimezone(pytz.utc), userid, repos)
            mylog.debug("total_count: " + str(total_count))

            pg.upsert_total_count(day.strftime("%Y-%m-%d"), userid, total_count)
    mylog.info("OK")


# 手動メンテナンス用
if __name__ == "__main__":
    # "2017-01-01"みたいにゼロ埋めしても支障ないが、タイプが面倒
    print("開始日付を入力してください. ex) 2018-1-1")
    start = input()
    print("終了日付を入力してください. ex) 2018-1-7")
    end = input()
    range_handler(start, end)
