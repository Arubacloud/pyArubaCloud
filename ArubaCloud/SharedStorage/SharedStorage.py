from ArubaCloud.SharedStorage.Requests import *
from ArubaCloud.SharedStorage.Models import SharedStorageModel, SharedStorageProtocols
from ArubaCloud.base import ArubaCloudService


class SharedStorage(ArubaCloudService):
    def __init__(self, ws_uri, username, password):
        super(SharedStorage, self).__init__(ws_uri, username, password)

    def _call(self, method, *args, **kwargs):
        return method(Username=self.username, Password=self.password, uri=self.ws_uri, *args, **kwargs)

    def get(self):
        """
        Retrieve the current configured SharedStorages entries
        :return: [list] List containing the current SharedStorages entries
        """
        request = self._call(GetSharedStorages)
        response = request.commit()
        return response['Value']

    def purchase_iscsi(self, quantity, iqn, name):
        so = SharedStorageModel(Quantity=quantity, Value=iqn, SharedStorageName=name,
                                SharedStorageProtocolType=SharedStorageProtocols.iSCSI)
        request = self._call(SetEnqueuePurchaseSharedStorage, SharedStorageObject=so)
        response = request.commit()
        return response['Value']
