# ハンドラ
# lambda_function.lambda_handler
from datetime import date
from datetime import datetime as dt
from datetime import timedelta
import logging
import sys
sys.path.insert(0, "../common/")
import postgres as pg
import pytz
import add_step_count as add


def lambda_handler(event, context):

    mylog = logging.getLogger("mylog")
    mylog.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(fmt)
    mylog.addHandler(ch)

    period_beginnig = dt.now(pytz.utc) - timedelta(days=1)
    mylog.debug("Period Beginning: " + str(period_beginnig))
    for userid in pg.get_users():
        userid = userid[0]
        repos = pg.get_repos(userid)
        total_count = add.get_addition_count(period_beginnig, userid, repos)
        mylog.debug("total_count: " + str(total_count))
        pg.upsert_total_count(dt.strftime(period_beginnig.astimezone(pytz.timezone("Asia/Tokyo")), '%Y-%m-%d'), userid, total_count)
    print("OK")


if __name__ == "__main__":
    lambda_handler(None, None)
