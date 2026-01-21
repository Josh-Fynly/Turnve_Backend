class Resource:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def consume(self, amount):
        if amount > self.quantity:
            raise Exception("Insufficient resource")
        self.quantity -= amount