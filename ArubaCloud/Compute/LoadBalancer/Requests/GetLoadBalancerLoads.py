from ArubaCloud.base import Request


class GetLoadBalancerLoads(Request):
    def __init__(self, startDate, endDate, loadBalancerID, *args, **kwargs):
        """
        Get the load balancer load within a specifying window time frame
        :type startDate: datetime
        :type endDate: datetime
        :type laodBalancerID: int
        :param startDate: From Date
        :param endDate: To Date
        :param loadBalancerID: ID of the LaodBalancer
        """
        self.StartDate = startDate
        self.EndDate = endDate
        self.LoadBalancerID = loadBalancerID
        super(GetLoadBalancerLoads, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
