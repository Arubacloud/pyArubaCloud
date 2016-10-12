from ArubaCloud.base import Request


class SetEnqueueLoadBalancerPowerOff(Request):
    def __init__(self, loadBalancerID, *args, **kwargs):
        self.LoadBalancerID = loadBalancerID
        super(SetEnqueueLoadBalancerPowerOff, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
