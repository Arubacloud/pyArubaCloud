from ArubaCloud.base import Request


class SetEnqueueRemoveSharedStorage(Request):
    def __init__(self, *args, **kwargs):
        """
        Enqueue Shared Storage Remove
        :type SharedStorageID: str
        :param SharedStorageID: (str) The ID of the Storage Resource
        """
        try:
            self.SharedStorageID = kwargs.pop('SharedStorageID')
        except KeyError:
            raise Exception('SharedStorageID cannot be Null.')
        super(SetEnqueueRemoveSharedStorage, self).__init__(*args, **kwargs)

    def commit(self):
        self._commit()
