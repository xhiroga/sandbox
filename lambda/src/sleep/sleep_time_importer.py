# -*- coding: utf-8 -*-

from datetime import datetime as dt
import logging
import os
import requests
import sys
sys.path.insert(0, "../common/")
import postgres as pg
import pytz


mylog = logging.getLogger("mylog")
mylog.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(fmt)
mylog.addHandler(ch)


def lambda_handler(event, context):
    # 自分しか使わないのでuseridは決め打ち.
    # 本当はyesterdayもuserの居住地域に合わせた方がいいんだけど、そんなことしない.
    yesterday = dt.strftime((dt.now(pytz.utc) - td(days=1)).astimezone(pytz.timezone("Asia/Tokyo")), '%Y-%m-%d')
    import_sleep_time(1, yesterday)
    mylog.info("OK")


def import_sleep_time(user_id, day):
    global mylog
    URL = "https://api.airtable.com/v0/{0}/Log?api_key={1}&filterByFormula=(DATESTR({{ParsedDate}})='{2}')"
    # {0}:App ID, {1}:Table Name(ex. Home/Work/etc...), {2}:API_KEY, {3}:Day(ex. 2018-01-21)
    # {}を.formatと併用するのであれば、{{}}と書く.

    app_id = os.environ["AIRTABLE_SLEEP_LOG_APP_ID"]
    key = os.environ["AIRTABLE_API_KEY"]
    res = requests.get(URL.format(app_id, key, day)).json()
    mylog.info(res)
    if res["records"] == []:
        mylog.info("no records. stop program.")
        return

    sum_time_slept, sum_time_ofrestfully_slept = measure_sleep_time(res)
    mylog.debug("sum_time_slept: " + str(sum_time_slept))
    mylog.debug("sum_time_ofrestfully_slept: " + str(sum_time_ofrestfully_slept))

    pg.upsert_sleep_time(user_id, day, str(sum_time_slept), str(sum_time_ofrestfully_slept))


def measure_sleep_time(res):
    sum_time_slept_in_seconds = 0
    sum_time_ofrestfully_slept_in_seconds = 0
    for record in res["records"]:
        sum_time_slept_in_seconds += record["fields"]["TotalTimeSleptInSeconds"]
        sum_time_ofrestfully_slept_in_seconds += record["fields"]["TotalTimeOfRestfullySleptInSeconds"]

    mylog.debug("sum_time_slept_in_seconds: "+ str(sum_time_slept_in_seconds))
    mylog.debug("sum_time_ofrestfully_slept_in_seconds: " + str(sum_time_ofrestfully_slept_in_seconds))

    sum_time_slept = dt.fromtimestamp(sum_time_slept_in_seconds) - dt.fromtimestamp(0)
    sum_time_ofrestfully_slept = dt.fromtimestamp(sum_time_ofrestfully_slept_in_seconds) - dt.fromtimestamp(0)
    return(sum_time_slept, sum_time_ofrestfully_slept)


# 手動実行用
if __name__ == "__main__":
    print("対象の日付を入力してください. ex) 2018-01-01")
    day = input()
    # useridは決め打ち
    import_sleep_time(1, day)
    mylog.info("OK")

# メモ
# recordあり、なし、postgres重複、の3パターンテスト済。
