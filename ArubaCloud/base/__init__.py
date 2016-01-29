import json
from abc import ABCMeta

from ArubaCloud.helper import Http


class JsonInterfaceBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def gen_def_json_scheme(self, req, method_fields=None):
        """
        Generate the scheme for the json request.
        :param req: String representing the name of the method to call
        :param method_fields: A dictionary containing the method-specified fields
        :rtype : json object representing the method call
        """
        json_dict = dict(
            ApplicationId=req,
            RequestId=req,
            SessionId=req,
            Password=self.auth.password,
            Username=self.auth.username
        )
        if method_fields is not None:
            json_dict.update(method_fields)
        self.logger.debug(json.dumps(json_dict))
        return json.dumps(json_dict)

    def call_method_post(self, method, json_scheme, debug=False):
        url = '{}/{}'.format(self.wcf_baseurl, method)
        headers = {'Content-Type': 'application/json', 'Content-Length': len(json_scheme)}
        response = Http.post(url=url, data=json_scheme, headers=headers)
        parsed_response = json.loads(response.content)
        if response.status_code != 200:
            from ArubaCloud.base.Errors import MalformedJsonRequest
            raise MalformedJsonRequest("Request: {}, Status Code: {}".format(json_scheme, response.status_code))
        if parsed_response['Success'] is False:
            from ArubaCloud.base.Errors import RequestFailed
            raise RequestFailed("Request: {}, Response: {}".format(json_scheme, parsed_response))
        if debug is True:
            msg = "Response Message: {}\nHTTP Status Code: {}".format(parsed_response, response.status_code)
            self.logger.debug(msg)
            print(msg)
        return parsed_response


class Auth(object):
    username = None
    password = None
    token = None
    enc_pwd = None

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
