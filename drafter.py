import pandas, random, os

data = pandas.read_csv("set.csv")


basic_lands = data.query("type.str.contains('Basic Land')")
commons = data.query("rarity=='common' and not type.str.contains('Basic Land')")
uncommons = data[data.rarity=="uncommon"]
rares = data[data.rarity=="rare"]
mythics = data[data.rarity=="mythic"]
mythrares = mythics.append(rares)


def draft():
    return list(commons.sample(10, replace=True).append(
                uncommons.sample(3, replace=True)).append(
                    mythrares.sample())
                .uuid)

def nameprint(deck):
    for i in set(deck):
        print(deck.count(i), "x", data.query("uuid == @i")["name"].values[0])

if __name__ == "__main__":
    print("set statistics:")
    print("\tcommon:   ", len(commons))
    print("\tuncommon: ", len(uncommons))
    print("\trare:     ", len(rares))
    print("\tmythic:   ", len(mythics))
    print("\n")

    deck = draft()
    nameprint(deck)
    if "kitty" in os.environ["TERM"].lower():
        os.system(f"timg -p k --grid=4 {' '.join(map(lambda x : os.path.join('images', x), deck))}")

