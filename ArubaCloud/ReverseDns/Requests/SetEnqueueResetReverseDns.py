from .BaseReverseDns import BaseReverseDns


class SetEnqueueResetReverseDns(BaseReverseDns):
    def __init__(self, *args, **kwargs):
        super(SetEnqueueResetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()