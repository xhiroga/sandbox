from datetime import date
from datetime import datetime as dt
from datetime import timedelta
import add_step_count as add
import postgres as pg
import pandas as pd


def range_handler(start, end):

    for userid in pg.get_users():
        for t in pd.date_range(start, end):
            day = t.strftime("%Y-%m-%d")
            repos = pg.get_repos(userid)
            total_count = add.get_addition_count(day, userid, repos)
            pg.insert_total_count(day, userid, total_count)
    print("OK")


# 手動メンテナンス用
if __name__ == "__main__":
    # 本当は"2017-01-01"みたいにゼロ埋めしてもいいのだが、タイプ数が面倒
    print("開始日付を入力してください. ex) 2017-1-1")
    start = input()
    print("終了日付を入力してください. ex) 2017-1-7")
    end = input()
    range_handler(start, end)
