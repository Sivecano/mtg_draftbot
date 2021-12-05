class Collection:
    def __init__(self, cards=None):
        if isinstance(cards, list):
            self.data = {id : cards.count(id) for id in set(cards)}
        elif isinstance(cards, dict):
            self.data = cards.copy()
        elif isinstance(cards, str):
            with open(cards, "r") as file:
                self.data = {id : int(count) for id,count in (line.split(",") for line in file)}
        else:
            self.data = {}

    def to_csv(self, filename):
        with open(filename, "w") as file:
            for id in self.data:
                print(f"{id},{self.data[id]}", file=file)

    def add_card(self, card_id, amount = 1):
        if card_id in self.data:
            self.data[card_id] += amount
        else:
            self.data[card_id] = amount

    def remove_card(self, card_id, amount=1):
        if card_id in self.data:
            if self.data[card_id] > amount:
                self.data[card_id] -= amount
            else:
                del self.data[card_id]
    
    def get_amount(self, card_id):
        if card_id in self.data:
            return self.data[card_id]
        return 0




if __name__ == "__main__":
    import drafter
    c = Collection(drafter.draft())
    print(c.data)
    c.to_csv("aa.csv")
    c = Collection("aa.csv")
    print(c.data)




