import pandas, random, os

data = pandas.read_csv("set.csv")


#print({r : len(data[data.rarity==r]) for r in set(data.rarity)})

basic_lands = data.query("type.str.contains('Basic Land')")
commons = data.query("rarity=='common' and not type.str.contains('Basic Land')")
uncommons = data[data.rarity=="uncommon"]
rares = data[data.rarity=="rare"]
mythics = data[data.rarity=="mythic"]
mythrares = mythics.append(rares)
#print(mythrares)

def draft():
    return list(commons.sample(10, replace=True).append(
                uncommons.sample(3, replace=True)).append(
                    mythrares.sample())
                .uuid)

def nameprint(deck):
    for i in set(deck):
        print(deck.count(i), "x", data.query("uuid == @i")["name"].values[0])

if __name__ == "__main__":
    deck = draft()
    #print(data.query("uuid in @deck"))
    nameprint(deck)
    if "kitty" in os.environ["TERM"].lower():
        os.system(f"timg -p k --grid=4 {' '.join(map(lambda x : os.path.join('images', x), deck))}")

