from ArubaCloud.base import Request
from ArubaCloud.Compute.LoadBalancer.Models import NewLoadBalancerRule


class SetAddLoadBalancerRule(Request):
    def __init__(self, loadBalancerID, newLoadBalancerRule, *args, **kwargs):
        """
        :type loadBalancerID: int
        :type newLoadBalancerRule: NewLoadBalancerRule
        :param loadBalancerID: ID of the Laod Balancer
        :param newLoadBalancerRule: NotificationContacts object, or a list of NotificationContact
        """
        self.LoadBalancerID = loadBalancerID
        self.NewLoadBalancerRule = newLoadBalancerRule
        super(SetAddLoadBalancerRule, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
