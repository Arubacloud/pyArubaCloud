from ._BaseReverseDns import BaseReverseDns


class SetEnqueueResetReverseDns(BaseReverseDns):
    def __init__(self, *args, **kwargs):
        try:
            self.IPs = kwargs.pop('IPs')
        except KeyError:
            # IPs parameter is not filled
            self.IPs = []
        super(SetEnqueueResetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
