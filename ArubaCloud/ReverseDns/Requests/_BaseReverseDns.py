from ArubaCloud.base import Request


class BaseReverseDns(Request):
    def __init__(self, *args, **kwargs):
        """
        :param IPs: [list] List of IP to handle
        :type IPs: list
        """
        try:
            self.IPs = kwargs.pop('IPs')
        except KeyError:
            # IPs parameter is not filled
            self.IPs = []
        super(BaseReverseDns, self).__init__(*args, **kwargs)
        # noinspection PyPep8Naming

    def commit(self):
        pass
