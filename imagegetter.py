import requests, pandas, os, time

data = pandas.read_csv("set.csv")

cards = len(data)
current = 0

print(len(data))
print("      ", end="")

for (id, image) in zip(data["uuid"], data["image"]):
    with requests.get(image) as img:
        with open(os.path.join("images", id), "wb") as file:
            file.write(img.content)
    current += 1
    print(7*chr(8), end="")
    print(str(round(100*current / cards, 2)).zfill(5), "%", end="", flush=True)
    
print()

