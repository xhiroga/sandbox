import requests
from datetime import datetime as dt
from datetime import timedelta
import logging
import pytz


def get_addition_count(day, userid, repos):
    mylog = logging.getLogger("mylog")
    mylog.debug("userid")
    mylog.debug(userid)

    ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
    LIST_COMMITS_API = "https://api.github.com/repos/{0}/{1}/commits?since='{2}'"
    SINGLE_COMMIT_API = "https://api.github.com/repos/{0}/{1}/commits/{2}"

    total_count = 0

    t = dt.strptime(day, '%Y-%m-%d')
    dt_jst = pytz.timezone("Asia/Tokyo").localize(t)
    dt_utc = dt_jst.astimezone(pytz.utc)
    mylog.debug("dt_utc")
    mylog.debug(dt_utc)
    mylog.debug("dt_utc + timedelta(days=1)")
    mylog.debug(dt_utc + timedelta(days=1))

    for rp in repos:
        mylog.debug("repository:")
        mylog.debug(rp)
        commits = requests.get(LIST_COMMITS_API.format(rp[0], rp[1], dt.strftime(dt_utc, ISO8601))).json()
        # パラメータを複数指定することで対象commitを絞り込むこともできるのだが、そうするとresponseがなんか変になる...
        if "message" in commits: raise Exception(commits["message"])
        # APIのアクセス回数制限等の対策

        for cmt in commits:
            mylog.debug("commit:")
            mylog.debug(cmt["sha"])
            if "message" in cmt: raise Exception(cmt["message"])

            cmt_datetime = pytz.timezone('UTC').localize(dt.strptime(cmt["commit"]["author"]["date"], ISO8601))
            mylog.debug("commit datetime:")
            mylog.debug(cmt_datetime)
            mylog.debug("commit author loginuser:")
            mylog.debug(cmt["author"]["login"])
            if dt_utc <= cmt_datetime and cmt_datetime <= dt_utc + timedelta(days=1) and cmt["author"]["login"] == userid:
                commit = requests.get(SINGLE_COMMIT_API.format(rp[0],rp[1],cmt["sha"])).json()
                mylog.debug("count in this commit: " + str(commit["stats"]["additions"]))

                total_count += commit["stats"]["additions"]
    return total_count
