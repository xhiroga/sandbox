# -*- coding: utf-8 -*-

import os
import requests
import sys
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td
sys.path.insert(0, "../common/")
import pandas as pd
import postgres as pg
import pytz


def lambda_handler(event, context):
    # 自分しか使わないのでuseridは決め打ち.
    # 本当はyesterdayもuserの居住地域に合わせた方がいいんだけど、そんなことしない.
    yesterday = dt.strftime((dt.now(pytz.utc) - td(days=1)).astimezone(pytz.timezone("Asia/Tokyo")), '%Y-%m-%d')
    for location in ("Home", "Work"):
        import_spent_time(1, location, yesterday)
    print("OK")


def import_spent_time(userid, location, day):
    URL = "https://api.airtable.com/v0/{0}/{1}?api_key={2}&filterByFormula=(DATESTR({{ParsedDate}})='{3}')"
    # {0}:App ID, {1}:Table Name(ex. Home/Work/etc...), {2}:API_KEY, {3}:Day(ex. 2018-01-21)
    # {}を.formatと併用するのであれば、{{}}と書く.

    app_id = os.environ["AIRTABLE_LOCATION_TRACKING_APP_ID"]
    key = os.environ["AIRTABLE_API_KEY"]
    res = requests.get(URL.format(app_id, location, key, day)).json()
    print(location)
    print(res)
    spent_time = td()
    if res["records"] != []:
        spent_time = measure_spent_time(res, day)

    print("spent_time: " + str(spent_time))
    pg.upsert_spent_time(userid, location, day, str(spent_time))


def measure_spent_time(res, day):
    df = pd.DataFrame({"EnteredOrExited":record["fields"]["EnteredOrExited"], "ParsedDate":dt.strptime(record["fields"]["ParsedDate"],'%Y-%m-%dT%H:%M:%S.%fZ')} for record in res["records"])
    df = df.sort_values(by="ParsedDate").reset_index(drop=True)
    print(df)

    is_enter = True
    day_date = dt.strptime(day, "%Y-%m-%d")
    stride_time = day_date
    spent_time = td()

    for index, row in df.iterrows():
        if row["EnteredOrExited"] == "entered":
            is_enter = True
        if row["EnteredOrExited"] == "exited":
            is_enter = False
            spent_time += row["ParsedDate"] - stride_time
        stride_time = row["ParsedDate"]

    if is_enter:
        spent_time += day_date + td(days=1) - stride_time

    return spent_time


# 手動メンテナンス用
if __name__ == "__main__":
    print("対象の日付を入力してください. ex) 2018-01-01")
    day = input()
    for location in ("Home", "Work"):
        # useridは決め打ち
        import_spent_time(1, location, day)

    print("OK")
