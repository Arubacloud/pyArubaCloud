from ArubaCloud.base import Request


class GetSharedStorages(Request):
    def __init__(self, *args, **kwargs):
        super(GetSharedStorages, self).__init__(*args, **kwargs)

    def commit(self):
        self._commit()
