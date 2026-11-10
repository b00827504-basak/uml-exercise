"""A small ordering example based on the ABCD Records UML diagrams."""


class Member:
    def __init__(self, name):
        self.name = name

    def can_order_unavailable(self):
        return False

    def discount(self):
        return 0


class RegularMember(Member):
    pass


class RoyalMember(Member):
    def can_order_unavailable(self):
        return True

    def discount(self):
        return 0.10


class Item:
    def __init__(self, title, price, stock):
        self.title = title
        self.price = price
        self.stock = stock


class CD(Item):
    pass


class Tape(Item):
    pass


class Order:
    def __init__(self, member):
        self.member = member
        self.lines = []
        self.status = "new"

    def add_item(self, item, quantity):
        if item.stock < quantity and not self.member.can_order_unavailable():
            return False
        self.lines.append((item, quantity))
        return True

    def total(self):
        amount = sum(item.price * quantity for item, quantity in self.lines)
        return round(amount * (1 - self.member.discount()), 2)


class Payment:
    def pay(self, amount):
        raise NotImplementedError


class Cash(Payment):
    def pay(self, amount):
        return True


class Check(Payment):
    def pay(self, amount):
        return True


class BankDraft(Payment):
    def pay(self, amount):
        return True


class OrderProcessingClerk:
    def process(self, order):
        order.status = "ready for payment"
        return order.total()


class CollectionDepartmentClerk:
    def collect(self, order, payment):
        if payment.pay(order.total()):
            order.status = "paid"
            return True
        return False


if __name__ == "__main__":
    member = RoyalMember("Taylor")
    cd1 = CD("Album A", 12, 3)
    cd2 = CD("Album B", 15, 0)
    order = Order(member)

    print("First CD accepted:", order.add_item(cd1, 1))
    print("Unavailable CD accepted:", order.add_item(cd2, 1))
    clerk = OrderProcessingClerk()
    print("Total with Royal discount:", clerk.process(order))

    collection = CollectionDepartmentClerk()
    print("Paid by check:", collection.collect(order, Check()))
    print("Order status:", order.status)
