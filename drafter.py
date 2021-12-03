import pandas, random, os

data = pandas.read_csv("set.csv")


print({r : len(data[data.rarity==r]) for r in set(data.rarity)})

basic_lands = data.query("type.str.contains('Basic Land')")
commons = data.query("rarity=='common' and not type.str.contains('Basic Land')")
uncommons = data[data.rarity=="uncommon"]
rares = data[data.rarity=="rare"]
mythics = data[data.rarity=="mythic"]
mythrares = mythics.append(rares)
#print(mythrares)

deck = commons.sample(10, replace=True).append(uncommons.sample(3, replace=True)).append(mythrares.sample())
print(deck)

os.system(f"timg -p k --grid=4 {' '.join(map(lambda x : os.path.join('images', x), list(deck.uuid)))}")

