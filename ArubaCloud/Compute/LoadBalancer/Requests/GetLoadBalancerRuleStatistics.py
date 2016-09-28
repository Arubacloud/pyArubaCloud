from ArubaCloud.base import Request


class GetLoadBalancerRuleStatistics	(Request):
    def __init__(self, startDate, endDate, loadBalancerRuleID, *args, **kwargs):
        """
        Get the load balancer rule statistics within a specified time frame
        :type startDate: datetime
        :type endDate: datetime
        :type loadBalancerRuleID: int
        :param startDate: From Date
        :param endDate: To Date
        :param loadBalancerRuleID: ID of the Load Balancer Rule
        """
        self.StartDate = startDate
        self.EndDate = endDate
        self.LoadBalancerRuleID = loadBalancerRuleID
        super(GetLoadBalancerRuleStatistics, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
