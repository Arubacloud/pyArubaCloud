from ArubaCloud.base import Request
from ArubaCloud.SharedStorage.Models import SharedStorage


class SetEnqueuePurchaseSharedStorage(Request):
    def __init__(self, SharedStorageObject, *args, **kwargs):
        """
        Purchase new SharedStorage Service
        :type SharedStorage: SharedStorage
        :param SharedStorage: (SharedStorage)
        """
        self.SharedStorage = SharedStorageObject.serialize()
        super(SetEnqueuePurchaseSharedStorage, self).__init__(*args, **kwargs)

    def commit(self):
        self._commit()
