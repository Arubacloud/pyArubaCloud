import unittest
from ArubaCloud.Compute.LoadBalancer import LoadBalancer
from . import ws_uri, username, password
from datetime import datetime, timedelta


class LoadBalancerTest(unittest.TestCase):
    def setUp(self):
        self.loadBalancer = LoadBalancer(ws_uri=ws_uri, username=username, password=password)

    def test_get(self):
        response = self.loadBalancer.get()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)

    def test_get_load_balancer_notifications(self):
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now()


if __name__ == '__main__':
    unittest.main()
