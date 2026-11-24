import unittest
from preview import preview

class Transport:
    def post(self, path, payload):
        assert path == '/preview'
        return {'subtotal': payload['unit_price_cents'] * payload['quantity']}

class PreviewTest(unittest.TestCase):
    def test_updates(self):
        self.assertEqual(preview({'unit_price_cents': 125}, 3, Transport()), 375)
