import json
from abc import ABCMeta
from collections import OrderedDict
from ArubaCloud.base import JsonInterfaceBase


class Creator(object):
    __metaclass__ = ABCMeta
    json_msg = OrderedDict()

    def get_raw(self):
        return self.json_msg

    def get_json(self):
        return json.dumps(self.json_msg)

    def commit(self, url, debug=False):
        from ArubaCloud.helper import Http
        url = '{}/{}'.format(url, 'SetEnqueuePurchaseSharedStorage')
        headers = {'Content-Type': 'application/json', 'Content-Length': len(self.get_json())}
        response = Http.post(url=url, data=self.get_json(), headers=headers)
        parsed_response = json.loads(response.content)
        if debug is True:
            print(parsed_response)
        if parsed_response["Success"]:
            return True
        return False


class StorageCreator(Creator):
    def __init__(self, name, protocol, space, iqn, DC, auth_obj):
        self.name = name
        self.protocol = protocol
        self.space = space
        self.iqn = iqn
        self.auth = auth_obj
        self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.6/WsEndUser.svc/json' % (str(DC))
        if 'ISCSI' in self.protocol:
            self.json_msg = {
                'ApplicationId': 'SetEnqueuePurchaseSharedStorage',
                'RequestId': 'SetEnqueuePurchaseSharedStorage',
                'SessionId': '',
                'Password': auth_obj.password,
                'Username': self.auth.username,
                'SharedStorage': {
                    'Quantity': self.space,
                    'Value': self.iqn,
                    'SharedStorageName': self.name,
                    'SharedStorageProtocolType': 'ISCSI'
                }
            }
        else:
            self.json_msg = {
                'ApplicationId': 'SetEnqueuePurchaseSharedStorage',
                'RequestId': 'SetEnqueuePurchaseSharedStorage',
                'SessionId': '',
                'Password': auth_obj.password,
                'Username': self.auth.username,
                'SharedStorage': {
                    'Quantity': self.space,
                    'SharedStorageName': self.name,
                    'SharedStorageProtocolType': self.protocol
                }
            }


class Storage_Actions(JsonInterfaceBase):

    def __init__(self, DC):
        super(Storage_Actions, self).__init__()
        self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.6/WsEndUser.svc/json' % (str(DC))

    @property
    def name(self):
        return self.name

    def get_shared_storage(self):
        scheme = self.gen_def_json_scheme('GetSharedStorages')
        json_obj = self.call_method_post('GetSharedStorages', json_scheme=scheme)
        return json_obj

    def remove_shared_storage(self, storageid):
        rm_storage_request = {
            "SetEnqueueRemoveSharedStorage": {
                "SharedStorageID": storageid
            }
        }
        scheme = self.gen_def_json_scheme('SetEnqueueRemoveSharedStorage', method_fields=rm_storage_request)
        json_obj = self.call_method_post('SetEnqueueRemoveSharedStorage', json_scheme=scheme)
        return json_obj

    def remove_iqn_storage(self, storageid):
        rm_storage_request = {
            "SetEnqueueRemoveIQNSharedStorage": {
                "SharedStorageID": storageid
            }
        }
        scheme = self.gen_def_json_scheme('SetEnqueueRemoveIQNSharedStorage', method_fields=rm_storage_request)
        json_obj = self.call_method_post('SetEnqueueRemoveIQNSharedStorage', json_scheme=scheme)
        return json_obj
