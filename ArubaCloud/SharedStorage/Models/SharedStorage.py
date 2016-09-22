import jsonpickle


class SharedStorageProtocols(object):
    iSCSI = "iSCSI"
    NFS = "NFS"


class SharedStorageModel(object):
    def __init__(self, Quantity=None, Value=None, SharedStorageName=None, SharedStorageProtocolType=None):
        """
        Initialize a new SharedStorage Model
        :param Quantity: (int) GB amount of GB
        :param Value: (str) Target IQN, nullable if not iSCSI
        :param SharedStorageName: (str) Name of the resource
        :param SharedStorageProtocolType: (SharedStorageProtocols) Type of Service (iSCSI, NFS)
        """
        assert isinstance(SharedStorageProtocolType, SharedStorageProtocols), Exception(
            'Excepted SharedStorageProtocolType, got: {}'.format(type(SharedStorageProtocolType))
        )
        self.Quantity = Quantity
        if SharedStorageProtocolType == SharedStorageProtocols.iSCSI:
            self.Value = Value
        self.SharedStorageName = SharedStorageName
        self.SharedStorageProtocolType = SharedStorageProtocolType

    def serialize(self):
        return jsonpickle.encode(self, unpicklable=False)
