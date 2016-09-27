from ArubaCloud.base import Request


class GetLoadBalancers(Request):
    def __init__(self, *args, **kwargs):
        super(GetLoadBalancers, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
