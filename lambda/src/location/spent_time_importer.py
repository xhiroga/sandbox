import os
import requests
import sys
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td
import pandas as pd
sys.path.insert(0, "../")
import postgres as pg


def lambda_handler(event, context):
    yesterday = dt.strftime(date.today() - timedelta(days=1), '%Y-%m-%d')
    # 自分しか使わないのでuseridは決め打ちにしておく.
    # for userid in pg.get_users():
    #     repos = pg.get_repos(userid)
    #     spent_time_importer.import_spent_time(yesterday, userid)
    spent_time_importer.import_spent_time(yesterday, 1)
    print("OK")


def import_spent_time(day, userid):

    URL = "https://api.airtable.com/v0/{0}/{1}?api_key={2}&filterByFormula=(DATESTR({{ParsedDate}})='{3}')"
    # {0}:App ID, {1}:Table Name(ex. Home/Work/etc...), {2}:API_KEY, {3}:Day(ex. 2018-01-21)
    # {}を.formatと併用するのであれば、{{}}と書く.

    app_id = os.environ["AIRTABLE_LOCATION_TRACKING_APP_ID"]
    location = "Home"
    key = os.environ["AIRTABLE_API_KEY"]

    res = requests.get(URL.format(app_id, location, key, day)).json()
    print(res)
    df = pd.DataFrame({"EnteredOrExited":record["fields"]["EnteredOrExited"], "ParsedDate":dt.strptime(record["fields"]["ParsedDate"],'%Y-%m-%dT%H:%M:%S.%fZ')} for record in res["records"])
    df = df.sort_values(by="ParsedDate").reset_index(drop=True)

    entered_time = dt.combine(date.today(), dt.min.time())
    spent_time = td()

    for index, row in df.iterrows():
        if row["EnteredOrExited"] == "entered":
            entered_time = row["ParsedDate"]
        else:
            spent_time += row["ParsedDate"] - entered_time
            entered_time = None
    if entered_time != None:
        spent_time += dt.combine(date.today(), dt.max.time()) - entered_time

    pg.upsert_spent_time(userid, location, day, str(spent_time))


# 手動メンテナンス用
if __name__ == "__main__":
    print("開始日付を入力してください. ex) 2018-1-1")
    # useridは決め打ち
    import_spent_time(input(), 1)
    print("OK")
