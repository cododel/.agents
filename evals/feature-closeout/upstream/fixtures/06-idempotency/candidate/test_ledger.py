import unittest
from ledger import Ledger

class LedgerTest(unittest.TestCase):
    def test_new_event(self):
        ledger = Ledger()
        self.assertEqual(ledger.handle({'id': 'evt1', 'amount_cents': 250}), 250)
        self.assertEqual(ledger.handle({'id': 'evt2', 'amount_cents': 100}), 350)
