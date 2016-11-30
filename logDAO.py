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
def writeLog(jsonString):
    dictString = json.loads(jsonString)
    if dictString.has_key(""):
        cur = conn.cursor()


'''
if __name__ == "__main__":
    print (returnNote("neo4j"))
'''
