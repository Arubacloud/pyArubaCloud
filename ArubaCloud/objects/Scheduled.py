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
        url = '{}/{}'.format(url, 'SetAddServerScheduledOperation')
        headers = {'Content-Type': 'application/json', 'Content-Length': len(self.get_json())}
        response = Http.post(url=url, data=self.get_json(), headers=headers)
        parsed_response = json.loads(response.content)
        if debug is True:
            print(parsed_response)
        if parsed_response["Success"]:
            return True
        return False


class Scheduled(JsonInterfaceBase):
    def __init__(self, DC):
        super(Scheduled, self).__init__()
        self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc/json' % (str(DC))

    @property
    def name(self):
        return self.name

    def get_scheduled_operations(self, start, end):
        
        get_shed_ops_request = {
            "GetScheduledOperations": {
                "EndDate": end,
                "StartDate": start
            }
        }
        scheme = self.gen_def_json_scheme('GetScheduledOperations', method_fields=get_shed_ops_request)
        json_obj = self.call_method_post('GetScheduledOperations', json_scheme=scheme)
        return json_obj

    def suspend_scheduled_operation(self, operationid):
        suspend_request = {
            "SetUpdateServerScheduledOperation": {
                "ScheduledOperationId": operationid
            }
        }
        scheme = self.gen_def_json_scheme('SetUpdateServerScheduledOperation', method_fields=suspend_request)
        json_obj = self.call_method_post('SetUpdateServerScheduledOperation', json_scheme=scheme)
        return True if json_obj['Success'] is True else False

    def delete_scheduled_operation(self, operationid):
        delete_request = {
            "SetRemoveServerScheduledOperation": {
                "ScheduledOperationId": operationid
            }
        }
        scheme = self.gen_def_json_scheme('SetRemoveServerScheduledOperation', method_fields=delete_request)
        json_obj = self.call_method_post('SetRemoveServerScheduledOperation', json_scheme=scheme)
        return True if json_obj['Success'] is True else False


class ScheduledCreator(Creator):
    def __init__(self, name, serverid, operationtype, start, end, DC, auth_obj):
        self.name = name
        self.serverid = serverid
        self.operationtype = ['CreateSnapshot', 'DeleteSnapshot', 'RestoreSnapShot',
                              'ShutdownVirtualMachine', 'StartVirtualMachine',
                              'StopVirtualMachine', 'UpdateVirtualMachine']
        for _optype_ in operationtype:
            if operationtype not in _optype_:
                raise Exception('error')
        self.start = start
        self.end = end
        self.auth = auth_obj
        self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc/json' % (str(DC))
        self.json_msg = {
            'ApplicationId': 'SetAddServerScheduledOperation',
            'RequestId': 'SetAddServerScheduledOperation',
            'SessionId': '',
            'Password': auth_obj.password,
            'Username': self.auth.username,
            'SetAddServerScheduledOperation': {
                'ScheduledOperationTypes': self.operationtype,
                'ScheduleOperationLabel': self.name,
                'ServerID': self.serverid,
                'ScheduleStartDateTime': self.start,
                'ScheduleEndDateTime': self.end,
                'ScheduleFrequencyType': 'RunOnce',
                'ScheduledPlanStatus': 'Enabled',
                'ScheduledMontlyRecurrence': 'FirstDay'
            }
        }
