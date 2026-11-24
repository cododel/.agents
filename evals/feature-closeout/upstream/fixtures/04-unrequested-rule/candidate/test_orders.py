import unittest
from orders import details

class OrdersTest(unittest.TestCase):
    def test_pending(self):
        order = {'id': 1, 'status': 'pending'}
        self.assertEqual(details(order, 5), {'id': 1, 'status': 'pending', 'elapsed_minutes': 5})
