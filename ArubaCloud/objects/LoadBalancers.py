import string

from ArubaCloud.base import Auth
from ArubaCloud.base import JsonInterfaceBase


# preparing the mess
def strfunc(self):
    classStr = ''
    for name, value in self.__class__.__dict__.items() + self.__dict__.items():
        classStr += string.ljust(name, 15) + '\t' + str(value) + '\n'
    return classStr


def reprfunc(self):
    return "<%s instance at %s>" % (self.__class__.__name__, id(self))


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
