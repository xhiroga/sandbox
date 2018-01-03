# ハンドラ
# lambda_function.lambda_handler
from datetime import date
from datetime import datetime as dt
from datetime import timedelta
import add_step_count as add
import postgres as pg


def lambda_handler(event, context):
    yesterday = dt.strftime(date.today() - timedelta(days=1), '%Y-%m-%d')
    for userid in pg.get_users():
        repos = pg.get_repos(userid)
        total_count = add.get_addition_count(yesterday, userid, repos)
        pg.insert_total_count(yesterday, userid, total_count)
    print("OK")


if __name__ == "__main__":
    lambda_handler(None, None)
