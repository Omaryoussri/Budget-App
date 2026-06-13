class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def __str__(self):
        output = f"{self.name:*^30}\n"
        for item in self.ledger:
            desc = item['description'][:23]
            amt = f"{item['amount']:.2f}"
            output += f"{desc:<23}{amt:>7}\n"
        output += f"Total: {self.get_balance():.2f}"
        return output


def create_spend_chart(categories):
    spent_per_category = []
    for category in categories:
        spent = sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        spent_per_category.append(spent)

    total_spent = sum(spent_per_category)

    percentages = []
    for spent in spent_per_category:
        if total_spent == 0:
            percentages.append(0)
        else:
            percentages.append(int((spent / total_spent) * 100 // 10) * 10)

    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| "
        for percent in percentages:
            if percent >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    max_len = max(len(category.name) for category in categories)
    names = [category.name for category in categories]

    for i in range(max_len):
        chart += "     "
        for name in names:
            if i < len(name):
                chart += f"{name[i]}  "
            else:
                chart += "   "
        if i < max_len - 1:
            chart += "\n"

    return chart


# --- Test the Implementation ---
food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)

print(food)
print("\n")
print(create_spend_chart([food, clothing]))