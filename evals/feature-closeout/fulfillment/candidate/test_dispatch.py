import unittest

from dispatch import tick


class DeliveryTest(unittest.TestCase):
    def test_dispatches_completed_purchase(self):
        purchase = {"id": "P1", "state": "pending", "job": "J1", "destination": "D1"}
        result = {"job": "J1", "kind": "original", "playable": True, "private_url": "synthetic-asset"}
        sent = []
        tick(purchase, True, result, lambda *args: sent.append(args), [])
        self.assertEqual(sent, [("D1", "synthetic-asset")])
        self.assertEqual(purchase["state"], "delivered")
