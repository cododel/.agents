class Ledger:
    def __init__(self):
        self.balance = 0
    def handle(self, event):
        self.balance += event['amount_cents']
        return self.balance
