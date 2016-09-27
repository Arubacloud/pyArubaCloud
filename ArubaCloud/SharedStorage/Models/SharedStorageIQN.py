from SharedStorageStatus import SharedStorageStatus


class SharedStorageIQNID(object):
    def __init__(self, iqnid=0, Status=SharedStorageStatus.Active, Value=""):
        """
        Initialize a new IQN Object
        :type iqnid: int
        :type Status: str
        :type Value: str
        :param iqnid: IQNid
        :param Status: default 'Active'
        :param Value: Target IQN
        """
        self.SharedStorageIQNID = iqnid
        self.Status = Status
        self.Value = Value
