from ArubaCloud.base import Request
from ArubaCloud.SharedStorage.Models import SharedStorageIQNID, SharedStorageProtocolType


class SetEnqueuePurchaseSharedStorage(Request):
    def __init__(self, *args, **kwargs):
        """
        Purchase new SharedStorage Service
        :type Quantity: int
        :type SharedStorageName: str
        :type SharedStorageProtocolType: SharedStorageProtocols
        :type SharedStorageIQNs: list[SharedStorageIQNID]
        :param Quantity: Amount of GB
        :param SharedStorageName: The name of the resource
        :param SharedStorageProtocolType: the object representing the protocol to instantiate
        """
        try:
            self.Quantity = kwargs.pop('Quantity')
            self.SharedStorageName = kwargs.pop('SharedStorageName')
            self.SharedStorageProtocolType = kwargs.pop('SharedStorageProtocolType') \
                if 'SharedStorageProtocolType' in kwargs.keys() else SharedStorageProtocolType.ISCSI
            self.SharedStorageIQNs = kwargs.pop('SharedStorageIQNs')
        except KeyError as e:
            raise Exception('{} cannot be null.'.format(e.message))
        super(SetEnqueuePurchaseSharedStorage, self).__init__(*args, **kwargs)

    def commit(self):
        self._commit()
