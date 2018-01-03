from datetime import date
from datetime import datetime as dt
import add_step_count as add
import postgres as pg


def test_handler(day, userid):
    repos = pg.get_repos(userid)
    total_count = add.get_addition_count(day, userid, repos)
    pg.insert_total_count(day, userid, total_count)
    print("OK")


if __name__ == "__main__":
    print("日付をYYYY-MM-DD形式で入力してください.")
    day = input()
    print("GitHubのユーザーIDを入力して下さい.")
    userid=input()
    test_handler(day, userid)

