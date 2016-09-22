from .BaseReverseDns import BaseReverseDns


class SetEnqueueSetReverseDns(BaseReverseDns):
    def __init__(self, *args, **kwargs):
        self.Hosts = kwargs.pop('Hosts')
        super(SetEnqueueSetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()