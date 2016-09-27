from ArubaCloud.base import ArubaCloudService


class LoadBalancer(ArubaCloudService):
    def __init__(self, *args, **kwargs):
        super(LoadBalancer, self).__init__(*args, **kwargs)
        pass

    def _call(self, method, *args, **kwargs):
        return method(Username=self.username, Password=self.password, uri=self.ws_uri, *args, **kwargs)

    def get(self):
        pass


