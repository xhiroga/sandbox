import random

import send
import logDAO
import seDAO

"""
def quizHandler(data):

# quizモードで呼ばれる


# SKET DANCE
def enigman():
    # イントロ

    # 1. イントロ >> 出題
    # 2. 採点 >> 再出題
    # 3. 採点 >> アウトロ

    # 初回以外
    judge(sender, yourAns, time):

    # 選題
    choiceQuiestion(sender):

    # 出題
    generateQuiz(quiz):

    # 成績格納

    # アウトロ

# 出題
def choiceQuestion():
    # 出題チョイス
    id = random.randint(1,300)
    return id

    #
# quizidをキーに、question, answer, optionをもらう
def generateQuiz():
    # 将来的にはquizidをキーにしてcypher"クエリ"を取ってくるが、今回はquizidからname, answerはnoteでcypherをそのまま発行する。


# イントロダクション for 1分モード
    # 初期化を呼ぶ

# イントロダクション for エンドレスモード
    # 開始
    # 終了の場合のメニュー


# 正誤判定
def judge(sender, yourAns, time):
    # 最終問題IDを取得（当面は問題の回答そのものを格納する）
    result = logDAO.getLastQuiz(sender)
    myAns = result[0]
    point = 0
    if (yourAns == myAns):
        point = 1
    #Quiz成績TBLに書き込み
    logDAO.setEvalation(quizid, sender, yourAns, point, ansDate)

    return point

#クイズ結果格納

# 誰が、どのクイズに対して、 なんと答え、正否、回答にかかった時間


# クイズモード終了

# 初期化

## DBに持っているもの
# クイズ形態
# 最後に出題した問題

"""
