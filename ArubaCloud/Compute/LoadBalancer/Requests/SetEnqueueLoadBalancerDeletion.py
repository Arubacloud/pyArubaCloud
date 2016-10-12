from ArubaCloud.base import Request


class SetEnqueueLoadBalancerDeletion(Request):
    def __init__(self, loadBalancerID, *args, **kwargs):
        self.LoadBalancerId = loadBalancerID
        super(SetEnqueueLoadBalancerDeletion, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
