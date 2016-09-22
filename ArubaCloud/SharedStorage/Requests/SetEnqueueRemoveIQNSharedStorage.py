from ArubaCloud.base import Request


class SetEnqueueRemoveIQNSharedStorage(Request):
    def __init__(self, *args, **kwargs):
        try:
            self.SharedStorageID = kwargs.pop('SharedStorageID')
        except KeyError:
            raise Exception('SharedStorageID cannot be Null.')
        super(SetEnqueueRemoveIQNSharedStorage, self).__init__(*args, **kwargs)

    def commit(self):
        self._commit()
