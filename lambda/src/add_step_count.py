import requests
from datetime import date
from datetime import datetime as dt
from datetime import timedelta
import pytz


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
