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


# noinspection PyPep8Naming
class GetReverseDns(BaseReverseDns):
    def __init__(self, *args, **kwargs):
        super(GetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()


class SetEnqueueResetReverseDns(Request):
    def __init__(self, *args, **kwargs):
        super(SetEnqueueResetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()


class SetEnqueueSetReverseDns(Request):
    def __init__(self, *args, **kwargs):
        self.Hosts = kwargs.pop('Hosts')
        super(SetEnqueueSetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
