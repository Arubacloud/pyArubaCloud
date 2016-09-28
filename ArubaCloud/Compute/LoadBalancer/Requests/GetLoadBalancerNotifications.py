from ArubaCloud.base import Request
from datetime import datetime


class GetLoadBalancerNotifications	(Request):
    def __init__(self, startDate, endDate, loadBalancerID, loadBalancerRuleID, *args, **kwargs):
        """
        Get the load balancer notifications for a specific rule within a specifying window time frame
        :type startDate: datetime
        :type endDate: datetime
        :type laodBalancerID: int
        :type loadBalancerRuleID: int
        :param startDate: From Date
        :param endDate: To Date
        :param loadBalancerID: ID of the Laod Balancer
        :param loadBalancerRuleID: ID of the Load Balancer Rule
        """
        self.StartDate = startDate
        self.EndDate = endDate
        self.LoadBalancerID = loadBalancerID
        self.LoadBalancerRuleID = loadBalancerRuleID
        super(GetLoadBalancerNotifications, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
