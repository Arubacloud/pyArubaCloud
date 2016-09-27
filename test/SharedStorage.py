import unittest
from ArubaCloud.SharedStorage import SharedStorage
from . import ws_uri, username, password


class ReverseDnsTest(unittest.TestCase):
    def setUp(self):
        self.sharedStorage = SharedStorage(ws_uri=ws_uri, username=username, password=password)

    def test_set_enqueue_purchase_shared_storage_iscsi(self):
        iqns = ['hsadfl.fsadf234f',
                'f34f34f.2f43f2f3f']
        response = self.sharedStorage.purchase_iscsi(quantity=100, name='TestSharedStorage', iqn=iqns)
        self.assertIsNotNone(response)

    def test_get_shared_storage(self):
        response = self.sharedStorage.get()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)

if __name__ == '__main__':
    unittest.main()
