import requests, json, os
import pandas

set = "m20" # 2020 core set
url = f"https://api.scryfall.com/cards/search?q=e:{set}"
more = True 
l = []

while more:
    with requests.get(url) as req:
        raw = json.loads(req.text)
    more = raw["has_more"]
    for i in raw["data"]:
        l.append({  "uuid"  :   i["oracle_id"], 
                    "set"   :   i["set"],
                    "rarity":   i["rarity"],
                    "image" :   i["image_uris"]["normal"],
                    "colours":  i["colors"],
                    "mana_cost":i["mana_cost"],
                    "name"  :   i["name"],
                    "type"  :   i["type_line"]
            })
    url = raw["next_page"]


data = pandas.DataFrame(l)

print(data)

data.to_json("set.json")





















