# ハンドラ
# lambda_function.lambda_handler
from datetime import date
from datetime import datetime as dt
import add_step_count as add
import postgres as pg


def lambda_handler():
    day = dt.strftime(date.today(), '%Y-%m-%d')
    for userid in pg.get_users():
        repos = pg.get_repos(userid)
        total_count = add.get_addition_count(day, userid, repos)
        pg.insert_total_count(day, userid, total_count)
    print("OK")


if __name__ == "__main__":
    lambda_handler()
