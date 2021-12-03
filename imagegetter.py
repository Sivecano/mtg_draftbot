import requests, pandas, os, time

data = pandas.read_csv("set.csv")

cards = len(data)
current = 0

print(len(data))
print("      ", end="")

for (id, image) in (zip(data["uuid"], data["image"])):
    with requests.get(image) as img:
        with open(os.path.join("images", id), "wb") as file:
            file.write(img.content)
    current += 1
    print(6*chr(8), end="")
    print(round(100*current / cards, 2), "%", end="", flush=True)
    time.sleep(0.07)
    


