class Ledger:
    def __init__(self):
        self.balance = 0
        self.seen = set()
    def handle(self, event):
        if event['id'] in self.seen:
            return
        self.balance += event['amount_cents']
        self.seen.add(event['id'])
