import unittest
from copy import deepcopy
from service import OrderSummaryService
from store import OrderStore

def order(id, tenant_id, currency, price, quantity):
    return {'id': id, 'tenant_id': tenant_id, 'currency': currency,
            'items': [{'quantity': quantity, 'unit_price_cents': price}]}

class SummaryTest(unittest.TestCase):
    def test_tenant_order_currency_and_read_only(self):
        records = [order('B', 'A', 'USD', 150, 2), order('A', 'A', 'EUR', 200, 2),
                   order('C', 'A', 'USD', 100, 1), order('A', 'B', 'USD', 999, 10)]
        before = deepcopy(records)
        service = OrderSummaryService(OrderStore(records))
        self.assertEqual(service.get('A'), {'count': 3, 'orders': [
            {'id': 'A', 'currency': 'EUR', 'total_cents': 400},
            {'id': 'B', 'currency': 'USD', 'total_cents': 300},
            {'id': 'C', 'currency': 'USD', 'total_cents': 100}],
            'totals_by_currency': {'EUR': 400, 'USD': 400}})
        self.assertEqual(records, before)
    def test_empty(self):
        self.assertEqual(OrderSummaryService(OrderStore([])).get('A'),
                         {'count': 0, 'orders': [], 'totals_by_currency': {}})
