import pandas, os

data = pandas.read_csv("set.csv")

mythics = data[data.rarity=='rare']

os.system(f"timg -p k --grid=3 {' '.join(map(lambda x : os.path.join('images', x), list(mythics.uuid)))}")

