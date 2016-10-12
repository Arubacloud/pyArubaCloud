from ArubaCloud.base import Request


class SetEnqueueLoadBalancerStart(Request):
    def __init__(self, loadBalancerID, *args, **kwargs):
        self.LoadBalancerId = loadBalancerID
        super(SetEnqueueLoadBalancerStart, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
