import unittest
from ArubaCloud.ReverseDns import ReverseDns
from . import ws_uri, username, password


class ReverseDnsTest(unittest.TestCase):
    def setUp(self):
        self.reverseDns = ReverseDns(ws_uri=ws_uri, username=username, password=password)

    def test_get_reverse_dns(self):
        response = self.reverseDns.get()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)

    def test_set_enqueue_set_reverse_dns(self):
        response = self.reverseDns.set(address='95.110.165.246', host_name=['myTestUnit.py'])
        self.assertIs(response, True)

    def test_set_enqueue_reset_reverse_dns(self):
        response = self.reverseDns.reset(address=['95.110.165.246'])
        self.assertIs(response, True)

if __name__ == '__main__':
    unittest.main()
