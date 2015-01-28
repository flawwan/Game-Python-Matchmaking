from lib.Database import Database
import math
import copy
from lib.Browser import Browser

db = Database()
import time
import json

browser = Browser()
db.query("""SELECT * FROM `matchmaking` WHERE `matchmaking_last_seen` > DATE_ADD(NOW(), INTERVAL - 3000 SECOND)""")

matchmaking = {}
for user in db.fetch_all():
    if matchmaking.get(user["matchmaking_node"]):
        matchmaking[user["matchmaking_node"]].append(user)
    else:
        matchmaking[user["matchmaking_node"]] = [user]

for active_node in matchmaking:
    # Fetch some information about the node
    db.query("""SELECT * FROM `nodes` WHERE `game_id`=%s""", [active_node])
    node_info = db.fetch()
    print node_info["game_name"]
    matches_possible = int(math.floor(len(matchmaking[active_node]) / node_info["game_players"]))
    # loop through each possible match
    for i in range(matches_possible):
        print "Match possible " + str(i)
        keys = []
        for x in range(node_info["game_players"]):
            db.query("UPDATE `matchmaking` SET `matchmaking_status` ='active' WHERE `matchmaking_id`=%s",
                     [matchmaking[active_node][0]["matchmaking_id"]])
            keys.append(matchmaking[active_node][0]["matchmaking_key"])
            del matchmaking[active_node][0]
        #Call the match server and tell it which players should compete
        try:
            browser.fetch(node_info["game_post_url"], {
                "keys": json.dumps(keys),
                "token": node_info["game_unique_hash"]
            })
            db.commit()
        except Exception as e:
            print "node down"
            db.rollback()