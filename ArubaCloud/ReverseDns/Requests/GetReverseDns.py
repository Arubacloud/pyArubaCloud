from ._BaseReverseDns import BaseReverseDns


# noinspection PyPep8Naming
class GetReverseDns(BaseReverseDns):
    def __init__(self, *args, **kwargs):
        try:
            self.IPs = kwargs.pop('IPs')
        except KeyError:
            # IPs parameter is not filled
            self.IPs = []
        super(GetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
