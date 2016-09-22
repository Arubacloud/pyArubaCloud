from ._BaseReverseDns import BaseReverseDns


# noinspection PyPep8Naming
class GetReverseDns(BaseReverseDns):
    def __init__(self, *args, **kwargs):
        super(GetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
