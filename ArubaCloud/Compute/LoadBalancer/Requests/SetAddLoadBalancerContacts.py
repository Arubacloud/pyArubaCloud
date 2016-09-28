from ArubaCloud.base import Request
from ArubaCloud.Compute.LoadBalancer.Models.NotificationContact import NotificationContact


class SetAddLoadBalancerContacts(Request):
    def __init__(self, loadBalancerID, notificationContacts, *args, **kwargs):
        """
        :type loadBalancerID: int
        :type notificationContacts: list[NotificationContact]
        :param loadBalancerID: ID of the Laod Balancer
        :param notificationContacts: NotificationContacts object, or a list of NotificationContact
        """
        self.LoadBalancerID = loadBalancerID
        self.NotificationContacts = notificationContacts
        super(SetAddLoadBalancerContacts, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
