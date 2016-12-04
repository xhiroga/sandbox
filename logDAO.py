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
    print (time)
    cur.execute("insert into messageLog (senderid, text, time) VALUES (%s, %s, %s);",(sender, text, datetime.fromtimestamp(time/1000)))
    cur.execute("select * from messageLog;")
    conn.commit()
    for row in cur.fetchall():
        print (row)

'''
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
