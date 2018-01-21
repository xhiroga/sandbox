import sys
from datetime import datetime as dt
import logging
import pandas as pd
sys.path.insert(0, "../")
import postgres as pg


def main(id):

    mylog = logging.getLogger("mylog")
    mylog.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(fmt)
    mylog.addHandler(ch)

    tz = "+0900"
    # 本来はidから取得すべき

    # tupelのリストを渡すまでがこのクラスの役割. multi-row insertはoDB依存処理.
    df = pd.read_csv("../../wrk/MoodnotesReport.csv")
    df = df[pd.notnull(df["Updated"])]
    args_list = [(id, row[3], row[5], dt.strptime(row[1], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S') + tz,
                  dt.strptime(row[2], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S') + tz) for row in df.values]
    # ex) [('1', 4.0, '今日は晴れだった', '2018-01-11 18:54:00+0900', '2018-01-11 18:57:00+0900'), (...), ...]

    pg.upsert_moodnotes(args_list)
    mylog.info("OK")


# To Be: get csv from AWS SES/ By Hand: get csv from local
if __name__ == "__main__":
    print("Input your id. ex) 1")
    id = input()
    main(id)
