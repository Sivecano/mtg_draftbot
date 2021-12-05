import requests, json, os, time
import pandas

set = "m20" # 2020 core set
url = f"https://api.scryfall.com/cards/search?q=e:{set}"
more = True 
l = []

while more:
    with requests.get(url) as req:
        raw = json.loads(req.text)
    # print(raw.keys())
    if (more := raw["has_more"]):
        url = raw["next_page"]
    for i in raw["data"]:
        l.append({  
                "uuid"      :   i["oracle_id"], 
                "set"       :   i["set"],
                "rarity"    :   i["rarity"],
                "card_id"   :   i["id"],
                "back_id"   :   i["card_back_id"],
                "colours"   :   i["colors"],
                "mana_cost" :   i["mana_cost"],
                "name"      :   i["name"],
                "type"      :   i["type_line"]
                })
    time.sleep(0.1)


data = pandas.DataFrame(l)

print(data)

data.to_csv("set.csv")





















