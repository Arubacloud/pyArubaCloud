from ArubaCloud.ReverseDns.Requests import *


class ArubaCloudService(object):
    def __init__(self, ws_uri, username, password, token=None):
        """
        :type ws_uri: str
        :type username: str
        :type password: str
        :type token: str
        :param ws_uri: WsEndUser URI
        :param username: ArubaCloud Service Username
        :param password: ArubaCloud Service Password
        :param token: Nullable, Token to be used instead of password
        """
        self.ws_uri = ws_uri
        self.username = username
        self.password = password
        self.token = token

    def login(self):
        raise NotImplemented('Not implemented yet...')

    def _call(self, method, *args, **kwargs):
        raise NotImplementedError


class ReverseDns(ArubaCloudService):
    def __init__(self, ws_uri, username, password):
        super(ReverseDns, self).__init__(ws_uri, username, password)

    def _call(self, method, *args, **kwargs):
        return method(Username=self.username, Password=self.password, uri=self.ws_uri, *args, **kwargs)

    def get(self):
        """
        Retrieve the current configured ReverseDns entries
        :return: [list] List containing the current ReverseDns Addresses
        """
        request = self._call(GetReverseDns)
        response = request.commit()
        return response['Value']

    def set(self, address, host_name):
        """
        :type address:  list[str]
        :type host_name: list[str]
        :param address: (list[str]) String representing the IP address to set
        :param host_name: (list[str]) Hostname to be assigned to reverse DNS
        :return: (bool) True in case of success, False in case of failure
        """
        request = self._call(SetEnqueueSetReverseDns, IPs=address, Hosts=host_name)
        response = request.commit()
        return response['Success']

    def reset(self, address=None):
        request = self._call(SetEnqueueResetReverseDns, IPs=address)
        response = request.commit()
        return response['Success']

