import unittest
from catalog import Catalog

class CatalogTest(unittest.TestCase):
    def test_cache_expiry_and_copy(self):
        now, calls = [0], []
        def provider():
            calls.append(now[0]); return ['A']
        c = Catalog(provider, lambda: now[0])
        c.get().append('X')
        now[0] = 59
        self.assertEqual(c.get(), ['A'])
        self.assertEqual(len(calls), 1)
        now[0] = 60
        self.assertEqual(c.get(), ['A'])
        self.assertEqual(len(calls), 2)
    def test_errors_not_cached(self):
        calls = []
        def provider():
            calls.append(1)
            if len(calls) == 1: raise RuntimeError('temporary')
            return ['A']
        c = Catalog(provider, lambda: 0)
        with self.assertRaises(RuntimeError): c.get()
        self.assertEqual(c.get(), ['A'])
        self.assertEqual(len(calls), 2)
