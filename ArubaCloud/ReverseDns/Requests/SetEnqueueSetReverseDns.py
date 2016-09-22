from ._BaseReverseDns import BaseReverseDns


class SetEnqueueSetReverseDns(BaseReverseDns):
    def __init__(self, Hosts, *args, **kwargs):
        self.Hosts = Hosts
        super(SetEnqueueSetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()