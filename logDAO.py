# PostgreSQLにアクセスログを格納する
# 将来的にはコネクション部分は分ける

import os
import psycopg2
import urllib.parse

from datetime import *

# connの確立
def geneConn():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn

def writeLog(sender, text, time):
    conn = geneConn()
    cur = conn.cursor()
    cur.execute("insert into messageLog (senderid, text, time) VALUES (%s, %s, %s);",(sender, text, datetime.fromtimestamp(time/1000)))
#    cur.execute("select * from messageLog;")
    conn.commit()
    conn.close()
#    for row in cur.fetchall():
#        print (row)

# senderからmodewを返す
def decideMode(sender):
    conn = geneConn()
    cur = conn.cursor()
    cur.execute("select mode from ChatMode where senderid = %s;",[sender])
    result = cur.fetchone()
    print (result)
    if (result == None):
        cur.execute("insert into ChatMode (senderid, mode) values (%s, %s);",(sender, "init"))
        conn.commit()
        conn.close()
        return "init"
    return result[0]

'''
def getLastQuiz(sender):
    conn = geneConn()
    cur = conn.cursor()
    cur.execute("select quizid from QuizStat where senderid = %s;", [sender])
    result = cur.fetchone()
    try
    raise StatNotExistError()

'''
'''
# 見本
{
    'entry':
    [{'id': '173247779792672', 'time': 1480509916595, 'messaging':
    [{'message': {'text': 'FreeBSD', 'seq': 1054, 'mid': 'mid.1480509916543:6a06f63681'}, 'timestamp': 1480509916543, 'recipient': {'id': '173247779792672'}, 'sender': {'id': '1071891079597615'}}]
    }],
    'object': 'page'
}
'''

'''
if __name__ == "__main__":
    time = 1480832602535
    time = time/1000
    writeLog(123456789012345, "this is test", time)
'''

'''
if __name__ == "__main__":
    print ("****** UT Start ******")
    # sender ß= "173247779792673"
    sender = "12345"
    print (decideMode(sender))
'''
