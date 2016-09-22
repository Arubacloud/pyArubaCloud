import unittest
from ArubaCloud.SharedStorage import SharedStorage
from . import ws_uri, username, password


class ReverseDnsTest(unittest.TestCase):
    def setUp(self):
        self.sharedStorage = SharedStorage(ws_uri=ws_uri, username=username, password=password)

    def test_get_shared_storage(self):
        response = self.sharedStorage.get()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)

if __name__ == '__main__':
    unittest.main()
