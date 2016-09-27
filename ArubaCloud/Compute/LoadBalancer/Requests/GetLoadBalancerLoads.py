from ArubaCloud.base import Request


class GetLoadBalancerLoads(Request):
    def __init__(self, startDate, endDate, loadBalancerID, *args, **kwargs):
        self.StartDate = startDate
        self.EndDate = endDate
        self.LoadBalancerID = loadBalancerID
        super(GetLoadBalancerLoads, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
