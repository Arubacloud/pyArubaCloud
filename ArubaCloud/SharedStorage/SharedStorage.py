from ArubaCloud.SharedStorage.Requests import *
from ArubaCloud.SharedStorage.Models import SharedStorageProtocolType, SharedStorageIQN
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

    def purchase_iscsi(self, quantity, iqn, name, protocol=SharedStorageProtocolType.ISCSI):
        """
        :type quantity: int
        :type iqn: list[str]
        :type name: str
        :type protocol: SharedStorageProtocols
        :param quantity: Amount of GB
        :param iqn: List of IQN represented in string format
        :param name: Name of the resource
        :param protocol: Protocol to use
        :return:
        """
        iqns = []
        for _iqn in iqn:
            iqns.append(SharedStorageIQN(Value=_iqn))
        request = self._call(SetEnqueuePurchaseSharedStorage, Quantity=quantity, SharedStorageName=name,
                             SharedStorageIQNs=iqns, SharedStorageProtocolType=protocol)
        response = request.commit()
        return response['Value']
