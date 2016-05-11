import string
import json
from abc import ABCMeta
from collections import OrderedDict
from collections import OrderedDict
from ArubaCloud.base import Auth
from ArubaCloud.base import JsonInterfaceBase
from ArubaCloud import PyArubaAPI


# preparing the mess
def strfunc(self):
    classStr = ''
    for name, value in self.__class__.__dict__.items() + self.__dict__.items():
        classStr += string.ljust(name, 15) + '\t' + str(value) + '\n'
    return classStr


def reprfunc(self):
    return "<%s instance at %s>" % (self.__class__.__name__, id(self))


class Creator(object):
    __metaclass__ = ABCMeta
    json_msg = OrderedDict()

    def get_raw(self):
        return self.json_msg

    def get_json(self):
        return json.dumps(self.json_msg)

    def commit(self, url, debug=False):
        from ArubaCloud.helper import Http
        url = '{}/{}'.format(url, 'SetEnqueueLoadBalancerCreation')
        headers = {'Content-Type': 'application/json', 'Content-Length': len(self.get_json())}
        response = Http.post(url=url, data=self.get_json(), headers=headers)
        parsed_response = json.loads(response.content)
        if debug is True:
            print(parsed_response)
        if parsed_response["Success"]:
            return True
        return False


class LoadBalancer(JsonInterfaceBase):

    def __init__(self, DC):
        super(LoadBalancer, self).__init__()
        self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.6/WsEndUser.svc/json' % (str(DC))

    @property
    def name(self):
        return self._name

    def get(self):
        scheme = self.gen_def_json_scheme('GetLoadBalancers')
        json_obj = self.call_method_post('GetLoadbalancers', json_scheme=scheme)
        self.raw = json_obj['Value'][0]

    def login(self, username, password):
        self.auth = Auth(username, password)

    def objectify(self, d):
        """
        WARNING, EXPERIMENTAL METHOD DO NOT USE
        """
        for k, v in d.items():
            if isinstance(v, dict):
                setattr(self, k, self.objectify(v))
            elif isinstance(v, list) and len(v) > 0:
                # this is the funniest part
                name = None
                name = {'LoadBalancerRules': 'LoadBalancerRule',
                        'LoadBalancerIPAddresses': 'LoadBalancerIPAddress',
                        'Instances': 'Instance'}[k]
                new_list = []
                for elem in v:
                    # create the new class
                    assert name is not None, "class name is none"
                    base_cls_spec = {'name': name,
                                     '__repr__': classmethod(reprfunc),
                                     '__str__': classmethod(strfunc)}
                    new_cls = type(name, (object,), base_cls_spec)
                    # create attributes
                    for k1, v1 in elem.items():
                        setattr(new_cls, k1, v1)
                    new_list.append(new_cls)
                    # print('%s: %s' % (new_cls, dir(new_cls)))
                setattr(self, k, new_list)
            else:
                setattr(self, k, v)

    def get_loadbalancer(self, lbid):
        lb_request = {
            "GetLoadbalancers": {
                "LoadBalancerID": lbid
            }
        }
        scheme = self.gen_def_json_scheme('GetLoadBalancers', method_fields=lb_request)
        json_obj = self.call_method_post('GetLoadbalancers', json_scheme=scheme)
        return json_obj['Value'][0]

    def enable_loadbalancer(self, lbid):
        enable_lb_request = {
            "SetEnqueueLoadBalancerStart": {
                "loadBalancerID": lbid
            }
        }
        scheme = self.gen_def_json_scheme('SetEnqueueLoadBalancerStart', method_fields=enable_lb_request)
        json_obj = self.call_method_post('SetEnqueueLoadBalancerStart', json_scheme=scheme)
        return True if json_obj['Success'] is True else False

    def disable_loadbalancer(self, lbid):
        disable_lb_request = {
            "SetEnqueueLoadBalancerPowerOff": {
                "loadBalancerID": lbid
            }
        }
        scheme = self.gen_def_json_scheme('SetEnqueueLoadBalancerPowerOff', method_fields=disable_lb_request)
        json_obj = self.call_method_post('SetEnqueueLoadBalancerPowerOff', json_scheme=scheme)
        return True if json_obj['Success'] is True else False

    def delete_loadbalancer(self, lbid):
        delete_lb_request = {
            "SetEnqueueLoadBalancerDeletion": {
                "loadBalancerID": lbid
            }
        }
        scheme = self.gen_def_json_scheme('SetEnqueueLoadBalancerDeletion', method_fields=delete_lb_request)
        json_obj = self.call_method_post('SetEnqueueLoadBalancerDeletion', json_scheme=scheme)
        return True if json_obj['Success'] is True else False

    def get_loadbalancer_stats(self, ruleid, start, end):
        lb_stats_request = {
            "GetLoadBalancerRuleStatistics": {
                "EndTime": end,
                "LoadBalancerRuleID": ruleid,
                "StartTime": start
            }
        }
        scheme = self.gen_def_json_scheme('GetLoadBalancerRuleStatistics', method_fields=lb_stats_request)
        json_obj = self.call_method_post('GetLoadBalancerRuleStatistics', json_scheme=scheme)
        return json_obj

    def get_loadbalancer_loads(self, lbid, start, end):
        lb_loads_request = {
            "GetLoadBalancerLoads": {
                "LoadBalancerID": lbid,
                "EndTime": end,
                "StartTime": start
            }
        }
        scheme = self.gen_def_json_scheme('GetLoadBalancerLoads', method_fields=lb_loads_request)
        json_obj = self.call_method_post('GetLoadBalancerLoads', json_scheme=scheme)
        return json_obj

    def get_loadbalancer_notifs(self, lbid, ruleid, start, end):
        lb_notifs_request = {
            "GetLoadBalancerNotifications": {
                "LoadBalancerID": lbid,
                "LoadBalancerRuleID": ruleid,
                "EndTime": end,
                "StartTime": start
            }
        }
        scheme = self.gen_def_json_scheme('GetLoadBalancerNotifications', method_fields=lb_notifs_request)
        json_obj = self.call_method_post('GetLoadBalancerNotifications', json_scheme=scheme)
        return json_obj


class LoadBalancerCreator(Creator):
    def __init__(self, name, serverid, algorithm, protocol, lbport, serverport, contact, DC, auth_obj):
        self.name = name
        self.serverid = serverid
        self.algorithm = algorithm
        self.protocol = protocol
        self.lbport = lbport
        self.serverport = serverport
        self.contact = contact
        self.auth = auth_obj
        self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.6/WsEndUser.svc/json' % (str(DC))
        self.json_msg = {
            'ApplicationId': 'SetEnqueueLoadBalancerCreation',
            'RequestId': 'SetEnqueueLoadBalancerCreation',
            'SessionId': '',
            'Password': auth_obj.password,
            'Username': self.auth.username,
            'LoadBalancer': {
                'Name': self.name,
                'IPAddress': PyArubaAPI.CloudInterface(DC).purchase_ip(),
                'ContactValue': self.contact,
                'BalanceType': self.algorithm,
                'Protocol': self.protocol,
                'LoadBalancerPort': self.lbport,
                'InstancePort': self.serverport
            }
        }