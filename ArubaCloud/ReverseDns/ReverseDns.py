from ArubaCloud.ReverseDns.Requests import *
from ArubaCloud.base import ArubaCloudService


class ReverseDns(ArubaCloudService):
    def __init__(self, ws_uri, username, password):
        super(ReverseDns, self).__init__(ws_uri, username, password)

    def _call(self, method, *args, **kwargs):
        return method(Username=self.username, Password=self.password, uri=self.ws_uri, *args, **kwargs)

    def get(self, addresses):
        """
        :type addresses: list[str]
        :param addresses: (list[str]) List of addresses to retrieve their reverse dns
        Retrieve the current configured ReverseDns entries
        :return: (list) List containing the current ReverseDns Addresses
        """
        request = self._call(GetReverseDns.GetReverseDns, IPs=addresses)
        response = request.commit()
        return response['Value']

    def set(self, address, host_name):
        """
        Assign one or more PTR record to a single IP Address
        :type address: str
        :type host_name: list[str]
        :param address: (str) The IP address to configure
        :param host_name: (list[str]) The list of strings representing PTR records
        :return: (bool) True in case of success, False in case of failure
        """
        request = self._call(SetEnqueueSetReverseDns.SetEnqueueSetReverseDns, IP=address, Hosts=host_name)
        response = request.commit()
        return response['Success']

    def reset(self, addresses):
        """
        Remove all PTR records from the given address
        :type addresses: List[str]
        :param addresses: (List[str]) The IP Address to reset
        :return: (bool) True in case of success, False in case of failure
        """
        request = self._call(SetEnqueueResetReverseDns.SetEnqueueResetReverseDns, IPs=addresses)
        response = request.commit()
        return response['Success']
