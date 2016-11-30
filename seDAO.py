import os
from neo4j.v1 import GraphDatabase, basic_auth

# about Environment
def envDriver():
    graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
    graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
    graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
    driver = GraphDatabase.driver(graphenedb_url, auth=basic_auth(graphenedb_user, graphenedb_pass))
    return driver

# 受け取ったクエリをそのままneo4jに流す
def neo4jThroughPass(query):
    graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
    graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
    graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
    driver = GraphDatabase.driver(graphenedb_url, auth=basic_auth(graphenedb_user, graphenedb_pass))
    session = driver.session()
    result = session.run(query)
    session.close()
    print ("GOAL!")

# 単語に対してnoteを返す
def returnNote(word):
    driver = envDriver()
    session = driver.session()
    result = session.run("MATCH (sw:Software) WHERE sw.Name = '" + word + "' RETURN sw.Name, sw.Note")
    note = "解説がヒットしませんでした。"
    if result is not None:
        for record in result:
            print (record)
            note = record["sw.Note"]
    return note

'''
if __name__ == "__main__":
    print (returnNote("neo4j"))
'''
