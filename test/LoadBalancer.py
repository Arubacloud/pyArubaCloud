import unittest
from ArubaCloud.Compute.LoadBalancer import LoadBalancer
from ArubaCloud.Compute.LoadBalancer.Models import NotificationContact, NotificationContacts, NotificationType, Rules, \
    NewLoadBalancerRule, LoadBalancerAlgorithmType, LoadBalancerProtocol, Instance
from . import ws_uri, username, password
from datetime import datetime, timedelta


class LoadBalancerTest(unittest.TestCase):
    def setUp(self):
        self.loadBalancer = LoadBalancer(ws_uri=ws_uri, username=username, password=password)

    def test_get(self):
        response = self.loadBalancer.get()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)

    # def test_get_load_balancer_notifications(self):
    #     start_date = datetime.now() - timedelta(days=1)
    #     end_date = datetime.now()

    # noinspection PyPep8Naming
    def test_set_enqueue_load_balancer_creation(self):
        """
        def __init__(self, healthCheckNotification, instance, ipAddressResourceId, loadBalancerClassOfServiceID, name,
                 notificationContacts, rules, *args, **kwargs):

        :return:
        """
        healthCheckNotification = True
        instance = [Instance(ipAddress='127.0.0.1')]
        ipAddressResourceId = 14211
        name = 'testUnitLoadBalancer'
        notificationContact = NotificationContact(contactValue='test@test.com', contactType=NotificationType.Email,
                                                  loadBalancerContactID=124142)
        notificationContacts = [notificationContact]
        rule = NewLoadBalancerRule(balancerType=LoadBalancerAlgorithmType.LeastConn,
                                   certificate='',
                                   instancePort=80,
                                   loadBalancerPort=80,
                                   protocol=LoadBalancerProtocol.Tcp,
                                   id=1,
                                   creationDate=datetime.now())
        rules = [rule]
        response = self.loadBalancer.create(
            healthCheckNotification=healthCheckNotification,
            instance=instance,
            ipAddressResourceId=[ipAddressResourceId],
            name=name,
            notificationContacts=notificationContacts,
            rules=rules
        )

        if __name__ == '__main__':
            unittest.main()
