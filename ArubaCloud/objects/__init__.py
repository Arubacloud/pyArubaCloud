import json
from abc import ABCMeta
from collections import OrderedDict

from ArubaCloud.base.Errors import ValidationError


class Creator(object):
    __metaclass__ = ABCMeta
    json_msg = OrderedDict()

    def get_raw(self):
        return self.json_msg

    def get_json(self):
        return json.dumps(self.json_msg)

    def commit(self, url, debug=False):
        from ArubaCloud.helper import Http
        url = '{}/{}'.format(url, 'SetEnqueueServerCreation')
        headers = {'Content-Type': 'application/json', 'Content-Length': str(len(self.get_json()))}
        response = Http.post(url=url, data=self.get_json(), headers=headers)
        if response.status_code != 200:
            print(response.content)
            return False
        parsed_response = json.loads(response.content)
        if debug is True:
            print(parsed_response)
        if parsed_response["Success"]:
            return True
        return False


class ProVmCreator(Creator):
    def __init__(self, name, admin_password, template_id, auth_obj, note=None):
        self.name = name
        self.admin_password = admin_password
        self.template_id = template_id
        self.auth = auth_obj
        self.note = 'Create by pyArubaCloud' if note is None else note
        self.ethernet_counter = 0
        self.virtual_disk_counter = 0
        self.json_msg = {
            'ApplicationId': 'SetEnqueueServerCreation',
            'RequestId': 'SetEnqueueServerCreation',
            'SessionId': '',
            'Password': auth_obj.password,
            'Username': self.auth.username,
            'Server': {
                'AdministratorPassword': self.admin_password,
                'CPUQuantity': 0,
                'Name': self.name,
                'NetworkAdaptersConfiguration': [],
                'Note': self.note,
                'OSTemplateId': self.template_id,
                'RAMQuantity': 0,
                'VirtualDisks': []
            }
        }

    def add_public_ip(self, public_ip_address_resource_id, primary_ip_address='true'):
        if self.ethernet_counter > 0:
            raise ValueError("Public IP Address must be bind to first Ethernet Interface.")
        network_adapter = {
            'NetworkAdapterType': self.ethernet_counter,
            'PublicIpAddresses': [{
                'PrimaryIPAddress': primary_ip_address,
                'PublicIpAddressResourceId': public_ip_address_resource_id
            }]
        }
        try:
            self.json_msg['Server']['NetworkAdaptersConfiguration'].append(network_adapter)
            self.ethernet_counter += 1
            return True
        except KeyError:
            return False

    def add_private_vlan(self, gateway, ip_address, private_vlan_resource_id, subnet_mask):
        if self.ethernet_counter > 2:
            raise ValueError("Cannot create more than 3 ethernet interface per VM.")
        network_adapter = {
            'NetworkAdapterType': self.ethernet_counter,
            'PrivateVLan': {
                'Gateway': gateway,
                'IPAddress': ip_address,
                'PrivateVLanResourceId': private_vlan_resource_id,
                'SubNetMask': subnet_mask
            }
        }
        try:
            self.json_msg['Server']['NetworkAdaptersConfiguration'].append(network_adapter)
            self.ethernet_counter += 1
            return True
        except KeyError:
            return False

    def add_virtual_disk(self, size):
        if self.virtual_disk_counter > 3:
            raise ValueError("Cannot create more than 4 disk.")
        if size > 500:
            raise ValueError("MaxSize per Disk: 500 GB.")
        virtual_disk = {
            "Size": size,
            "VirtualDiskType": self.virtual_disk_counter
        }
        try:
            self.json_msg['Server']['VirtualDisks'].append(virtual_disk)
            self.virtual_disk_counter += 1
            return True
        except KeyError:
            return False

    def set_cpu_qty(self, cpu_qty):
        self.json_msg['Server']['CPUQuantity'] = cpu_qty

    def set_ram_qty(self, ram_qty):
        self.json_msg['Server']['RAMQuantity'] = ram_qty
        
    def set_ssh_key(self, public_key_path):
        with open(public_key_path, 'r') as content_file:
            content = content_file.read()
        self.json_msg['Server']['SshKey'] = content
        self.json_msg['Server']['SshPasswordAuthAllowed'] = True


class SmartVmCreator(Creator):
    def __init__(self, name, admin_password, template_id, auth_obj, note=None):
        self.name = name
        self.admin_password = admin_password
        self.template_id = template_id
        self.auth_obj = auth_obj
        self.note = 'Create by pyArubaCloud' if note is None else note
        self.json_msg = {
            'ApplicationId': 'SetEnqueueServerCreation',
            'RequestId': 'SetEnqueueServerCreation',
            'Username': self.auth_obj.username,
            'Password': self.auth_obj.password,
            'Server': {
                'AdministratorPassword': self.admin_password,
                'Name': self.name,
                'SmartVMWarePackageID': 1,
                'Note': self.note,
                'OSTemplateId': self.template_id
            }
        }

    def set_type(self, package_id):
        """
        Define the size of the VM. Size available:
         - small
         - medium
         - large
         - extralarge
        :param size: str()
        :return:
        """
        self.json_msg['Server']['SmartVMWarePackageID'] = package_id
        return True
    
    
    def set_ssh_key(self, public_key_path):
        with open(public_key_path, 'r') as content_file:
            content = content_file.read()
        self.json_msg['Server']['SshKey'] = content
        self.json_msg['Server']['SshPasswordAuthAllowed'] = True


class Vlan(object):
    name = None
    resource_id = None
    vlan_code = None

    def __repr__(self):
        return 'Vlan(name={}, resource_id={}, vlan_code={})'.format(self.name, self.resource_id, self.vlan_code)

    def __str__(self):
        return 'Vlan(name={}, resource_id={}, vlan_code={})'.format(self.name, self.resource_id, self.vlan_code)


class NetworkAdapter(object):
    ip_addresses = []
    id = None
    mac_address = None
    network_adapter_type = None
    server_id = None
    vlan_id = None


class IpList(list):
    def __init__(self, *args):
        super(IpList, self).__init__(*args)

    def show(self):
        for elem in self:
            print(elem)

    def find(self, vm_name=None, ip_addr=None, resid=None):
        # more defensive checks, just to have fun...
        params = locals()
        pattern = {}
        ip = None
        for _item in params:
            if isinstance(params[_item], str) or isinstance(params[_item], int):
                pattern['criteria'] = _item
                pattern['value'] = params[_item]
        for elem in self:
            if not hasattr(elem, pattern['criteria']):
                raise ValidationError('The criteria specified does not exists: %s' % (pattern['criteria']))
            mtc = getattr(elem, pattern['criteria'])
            if mtc == pattern['value']:
                # we will return this object
                ip = elem
        # return the ip object which match the criteria
        assert (ip.__class__.__name__ is 'Ip' or ip is None), 'the returning object is not as expected.'
        return ip


class Ip(object):
    ip_addr = None
    resid = None
    serverid = None

    def __init__(self):
        pass

    def is_mapped(self):
        return True if self.serverid is not None else False


class VirtualDiskOperation(object):
    resize = 1
    create = 2
    delete = 3


class VirtualDisk(object):
    primary_disk_type = 3
    additional_disk1_type = 7
    additional_disk2_type = 8
    additional_disk3_type = 9
    primary_disk_id = 0
    additional_disk1_id = 1
    additional_disk2_id = 2
    additional_disk3_id = 3
