# PostgreSQLにアクセスログを格納する
# 将来的にはコネクション部分は分ける

import os
import psycopg2
import urllib

# connの確立
def geneConn():
    urllib.parse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

# 辞書オブジェクト.has_key(キー)
def writeLog(json):
    dict = json.loads(json)
    if dict["entry"][0]["messaging"][0].has_key("message"):
        senderid = dict["entry"][0]["messaging"][0]["sender"]["id"]
        text = dict["entry"][0][messaging][0][message][text]
        time = dict["entry"][0][messaging][0][timestamp]
        cur = conn.cursor("insert into (senderid, text, time) VALUES (%s, %s, %s;)",[senderid, text, time])

"""お手本
{
    'entry':
    [{'id': '173247779792672', 'time': 1480509916595, 'messaging':
    [{'message': {'text': 'FreeBSD', 'seq': 1054, 'mid': 'mid.1480509916543:6a06f63681'}, 'timestamp': 1480509916543, 'recipient': {'id': '173247779792672'}, 'sender': {'id': '1071891079597615'}}]
    }],
    'object': 'page'
}
"""


'''
if __name__ == "__main__":
    print (returnNote("neo4j"))
'''
