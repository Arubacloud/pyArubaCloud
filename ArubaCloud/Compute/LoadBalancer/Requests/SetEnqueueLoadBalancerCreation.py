from ArubaCloud.Compute.LoadBalancer.Models import Instance, Rules, NotificationContacts, NotificationContact
from ArubaCloud.base import Request


class SetEnqueueLoadBalancerCreation(Request):
    def __init__(self, healthCheckNotification, instance, ipAddressResourceId, loadBalancerClassOfServiceID, name,
                 notificationContacts, rules, *args, **kwargs):
        """
        :type healthCheckNotification: bool
        :type instance: Instance
        :type ipAddressResourceId: list[int]
        :type loadBalancerClassOfServiceID: int
        :type name: str
        :type notificationContacts: NotificationContacts or list[NotificationContact]
        :type rules: Rules
        :param healthCheckNotification:
        :param instance:
        :param ipAddressResourceId:
        :param loadBalancerClassOfServiceID:
        :param name:
        :param notificationContacts:
        :param rules:
        :param args:
        :param kwargs:
        """
        self.HealthCheckNotification = healthCheckNotification
        self.Instance = instance
        self.IpAddressResourceId = ipAddressResourceId
        self.LoadBalancerClassOfServiceID = loadBalancerClassOfServiceID
        self.Name = name
        self.NotificationContacts = notificationContacts
        self.Rules = rules
        super(SetEnqueueLoadBalancerCreation, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
