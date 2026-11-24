import unittest
from export import export_csv

class ExportTest(unittest.TestCase):
    def test_export(self):
        text = export_csv([{'order_id': 'A', 'amount_cents': 125, 'currency': 'USD'}])
        self.assertIn('A,125', text)
