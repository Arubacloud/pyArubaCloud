from ArubaCloud.base import Request


class BaseReverseDns(Request):
    def __init__(self, *args, **kwargs):
        """
        :param IPs: [list] List of IP to handle
        :type IPs: list
        """
        super(BaseReverseDns, self).__init__(*args, **kwargs)
        # noinspection PyPep8Naming
        IPs = kwargs.pop('IPs')
        self.IPs = IPs if IPs is not None else []

    def commit(self):
        pass
