import requests
from datetime import datetime as dt
from datetime import timedelta
import logging
import pytz


# day: awareなDateTime型(utc)とする。
def get_addition_count(day_time_utc, userid, repos):
    mylog = logging.getLogger("mylog")
    mylog.debug("Period Beginning: " + str(day_time_utc))
    mylog.debug("userid: " + userid)

    ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
    LIST_COMMITS_API = "https://api.github.com/repos/{0}/{1}/commits?since='{2}'"
    SINGLE_COMMIT_API = "https://api.github.com/repos/{0}/{1}/commits/{2}"

    total_count = 0

    for rp in repos:
        mylog.debug("repository: " + str(rp))
        commits = requests.get(LIST_COMMITS_API.format(rp[0], rp[1], dt.strftime(day_time_utc, ISO8601))).json()
        # パラメータを複数指定することで対象commitを絞り込むこともできるのだが、そうするとresponseがなんか変になる...
        if "message" in commits: raise Exception(commits["message"])
        # APIのアクセス回数制限等の対策

        for cmt in commits:
            if "message" in cmt: raise Exception(cmt["message"])
            mylog.debug("commit :" + str(cmt["sha"]))
            mylog.debug("commit author loginuser :" + str(cmt["author"]["login"]))
            cmt_datetime = pytz.timezone('UTC').localize(dt.strptime(cmt["commit"]["author"]["date"], ISO8601))
            mylog.debug("commit datetime: " + str(cmt_datetime))
            if day_time_utc <= cmt_datetime and cmt_datetime <= day_time_utc + timedelta(days=1) and cmt["author"]["login"] == userid:
                commit = requests.get(SINGLE_COMMIT_API.format(rp[0],rp[1],cmt["sha"])).json()
                mylog.debug("count in this commit: " + str(commit["stats"]["additions"]))

                total_count += commit["stats"]["additions"]
    return total_count
