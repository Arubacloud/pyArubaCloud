import logging
import sys
from pprint import pprint

from ArubaCloud.base import Auth, JsonInterfaceBase
from ArubaCloud.base.logsystem import ArubaLog
from ArubaCloud.base.vm import VMList
from ArubaCloud.objects import Ip, IpList, Vlan
from ArubaCloud.objects.Templates import Template
from ArubaCloud.objects.VmTypes import Pro, Smart


class JsonInterface(JsonInterfaceBase):
    pass


class LoadBalancer(JsonInterfaceBase):
    def __init__(self):
        super(LoadBalancer, self).__init__()
        self._name = ''
        self.auth = Auth()

    @property
    def name(self):
        return self._name

    def get(self):
        scheme = self.gen_def_json_scheme('GetLoadBalancers')
        json_obj = self.call_method_post('GetLoadbalancers', json_scheme=scheme)
        print(json_obj)

    def login(self, username, password):
        self.auth.username = username
        self.auth.password = password


class CloudInterface(JsonInterface):
    templates = []
    vmlist = VMList()
    iplist = IpList()
    json_templates = None
    json_servers = None
    ip_resource = None
    hypervisors = {3: "LC", 4: "SMART", 2: "VW", 1: "HV"}

    def __init__(self, dc, debug_level=logging.INFO):
        super(CloudInterface, self).__init__()
        assert isinstance(dc, int), Exception('dc must be an integer and must be not null.')
        self.wcf_baseurl = 'https://api.dc%s.computing.cloud.it/WsEndUser/v2.9/WsEndUser.svc/json' % (str(dc))
        self.logger = ArubaLog(level=debug_level, log_to_file=False)
        self.logger.name = self.__class__
        self.auth = None

    def login(self, username, password, load=True):
        """
        Set the authentication data in the object, and if load is True
        (default is True) it also retrieve the ip list and the vm list
        in order to build the internal objects list.
        @param (str) username: username of the cloud
        @param (str) password: password of the cloud
        @param (bool) load: define if pre cache the objects.
        @return: None
        """
        self.auth = Auth(username, password)
        if load is True:
            self.get_ip()
            self.get_servers()

    def poweroff_server(self, server=None, server_id=None):
        """
        Poweroff a VM. If possible to pass the VM object or simply the ID
        of the VM that we want to turn on.
        Args:
            server: VM Object that represent the VM to power off,
            server_id: Int or Str representing the ID of the VM to power off.
        Returns:
            return True if json_obj['Success'] is 'True' else False
        """
        sid = server_id if server_id is not None else server.sid
        if sid is None:
            raise Exception('No Server Specified.')
        json_scheme = self.gen_def_json_scheme('SetEnqueueServerPowerOff', dict(ServerId=sid))
        json_obj = self.call_method_post('SetEnqueueServerPowerOff', json_scheme=json_scheme)
        return True if json_obj['Success'] is 'True' else False

    def poweron_server(self, server=None, server_id=None):
        """
        Poweron a VM. If possible to pass the VM object or simply the ID
        of the VM that we want to turn on.
        Args:
            server: VM Object that represent the VM to power on,
            server_id: Int or Str representing the ID of the VM to power on.
        Returns:
            return True if json_obj['Success'] is 'True' else False
        """
        sid = server_id if server_id is not None else server.sid
        if sid is None:
            raise Exception('No Server Specified.')
        json_scheme = self.gen_def_json_scheme('SetEnqueueServerStart', dict(ServerId=sid))
        json_obj = self.call_method_post('SetEnqueueServerStart', json_scheme=json_scheme)
        return True if json_obj['Success'] is 'True' else False

    def get_hypervisors(self):
        """
        Initialize the internal list containing each template available for each
        hypervisor.

        :return: [bool] True in case of success, otherwise False
        """
        json_scheme = self.gen_def_json_scheme('GetHypervisors')
        json_obj = self.call_method_post(method='GetHypervisors', json_scheme=json_scheme)
        self.json_templates = json_obj
        d = dict(json_obj)
        for elem in d['Value']:
            hv = self.hypervisors[elem['HypervisorType']]
            for inner_elem in elem['Templates']:
                o = Template(hv)
                o.template_id = inner_elem['Id']
                o.descr = inner_elem['Description']
                o.id_code = inner_elem['IdentificationCode']
                o.name = inner_elem['Name']
                o.enabled = inner_elem['Enabled']
                if hv != 'SMART':
                    for rb in inner_elem['ResourceBounds']:
                        resource_type = rb['ResourceType']
                        if resource_type == 1:
                            o.resource_bounds.max_cpu = rb['Max']
                        if resource_type == 2:
                            o.resource_bounds.max_memory = rb['Max']
                        if resource_type == 3:
                            o.resource_bounds.hdd0 = rb['Max']
                        if resource_type == 7:
                            o.resource_bounds.hdd1 = rb['Max']
                        if resource_type == 8:
                            o.resource_bounds.hdd2 = rb['Max']
                        if resource_type == 9:
                            o.resource_bounds.hdd3 = rb['Max']
                self.templates.append(o)
        return True if json_obj['Success'] is 'True' else False

    def get_servers(self):
        """
        Create the list of Server object inside the Datacenter objects.
        Build an internal list of VM Objects (pro or smart) as iterator.
        :return: bool
        """
        json_scheme = self.gen_def_json_scheme('GetServers')
        json_obj = self.call_method_post(method='GetServers', json_scheme=json_scheme)
        self.json_servers = json_obj
        # if this method is called I assume that i must re-read the data
        # so i reinitialize the vmlist
        self.vmlist = VMList()
        # getting all instanced IP in case the list is empty
        if len(self.iplist) <= 0:
            self.get_ip()
        for elem in dict(json_obj)["Value"]:
            if elem['HypervisorType'] is 4:
                s = Smart(interface=self, sid=elem['ServerId'])
            else:
                s = Pro(interface=self, sid=elem['ServerId'])
            s.vm_name = elem['Name']
            s.cpu_qty = elem['CPUQuantity']
            s.ram_qty = elem['RAMQuantity']
            s.status = elem['ServerStatus']
            s.datacenter_id = elem['DatacenterId']
            s.wcf_baseurl = self.wcf_baseurl
            s.auth = self.auth
            s.hd_qty = elem['HDQuantity']
            s.hd_total_size = elem['HDTotalSize']
            if elem['HypervisorType'] is 4:
                ssd = self.get_server_detail(elem['ServerId'])
                try:
                    s.ip_addr = str(ssd['EasyCloudIPAddress']['Value'])
                except TypeError:
                    s.ip_addr = 'Not retrieved.'
            else:
                s.ip_addr = []
                for ip in self.iplist:
                    if ip.serverid == s.sid:
                        s.ip_addr.append(ip)
            self.vmlist.append(s)
        return True if json_obj['Success'] is True else False

    def find_template(self, name=None, hv=None):
        """
        Return a list of templates that could have one or more elements.
        Args:
            name: name of the template to find.
            hv: the ID of the hypervisor to search the template in
        Returns:
            A list of templates object. If hv is None will return all the
            templates matching the name if every hypervisor type. Otherwise
            if name is None will return all templates of an hypervisor.
        Raises:
            ValidationError: if name and hv are None
        """
        if len(self.templates) <= 0:
            self.get_hypervisors()
        if name is not None and hv is not None:
            template_list = filter(
                lambda x: name in x.descr and x.hypervisor == self.hypervisors[hv], self.templates
            )
        elif name is not None and hv is None:
            template_list = filter(
                lambda x: name in x.descr, self.templates
            )
        elif name is None and hv is not None:
            template_list = filter(
                lambda x: x.hypervisor == self.hypervisors[hv], self.templates
            )
        else:
            raise Exception('Error, no pattern defined')
        if  sys.version_info.major < (3):
            return template_list
        else:
            return(list(template_list))
        
    def get_vm(self, pattern=None):
        if len(self.vmlist) <= 0:
            self.get_servers()
        if pattern is None:
            return self.vmlist
        else:
            return self.vmlist.find(pattern)

    def get_ip_by_vm(self, vm):
        self.get_ip()  # call get ip list to create the internal list of IPs.
        vm_id = self.get_vm(vm)[0].sid
        for ip in self.iplist:
            if ip.serverid == vm_id:
                return ip
        return 'IPNOTFOUND'

    def purchase_ip(self, debug=False):
        """
        Return an ip object representing a new bought IP
        @param debug [Boolean] if true, request and response will be printed
        @return (Ip): Ip object
        """
        json_scheme = self.gen_def_json_scheme('SetPurchaseIpAddress')
        json_obj = self.call_method_post(method='SetPurchaseIpAddress', json_scheme=json_scheme, debug=debug)
        try:
            ip = Ip()
            ip.ip_addr = json_obj['Value']['Value']
            ip.resid = json_obj['Value']['ResourceId']
            return ip
        except:
            raise Exception('Unknown error retrieving IP.')

    def purchase_vlan(self, vlan_name, debug=False):
        """
        Purchase a new VLAN.
        :param debug: Log the json response if True
        :param vlan_name: String representing the name of the vlan (virtual switch)
        :return: a Vlan Object representing the vlan created
        """
        vlan_name = {'VLanName': vlan_name}
        json_scheme = self.gen_def_json_scheme('SetPurchaseVLan', vlan_name)
        json_obj = self.call_method_post(method="SetPurchaseVLan", json_scheme=json_scheme)
        if debug is True:
            self.logger.debug(json_obj)
        if json_obj['Success'] is False:
            raise Exception("Cannot purchase new vlan.")
        vlan = Vlan()
        vlan.name = json_obj['Value']['Name']
        vlan.resource_id = json_obj['Value']['ResourceId']
        vlan.vlan_code = json_obj['Value']['VlanCode']
        return vlan

    def remove_vlan(self, vlan_resource_id):
        """
        Remove a VLAN
        :param vlan_resource_id:
        :return:
        """
        vlan_id = {'VLanResourceId': vlan_resource_id}
        json_scheme = self.gen_def_json_scheme('SetRemoveVLan', vlan_id)
        json_obj = self.call_method_post(method='SetRemoveVLan', json_scheme=json_scheme)
        return True if json_obj['Success'] is True else False

    def get_vlan(self, vlan_name=None):
        json_scheme = self.gen_def_json_scheme('GetPurchasedVLans')
        json_obj = self.call_method_post(method='GetPurchasedVLans', json_scheme=json_scheme)
        if vlan_name is not None:
            raw_vlans = filter(lambda x: vlan_name in x['Name'], json_obj['Value'])
        else:
            raw_vlans = json_obj['Value']
        vlans = []
        for raw_vlan in raw_vlans:
            v = Vlan()
            v.name = raw_vlan['Name']
            v.vlan_code = raw_vlan['VlanCode']
            v.resource_id = raw_vlan['ResourceId']
            vlans.append(v)
        return vlans

    def remove_ip(self, ip_id):
        """
        Delete an Ip from the boughs ip list
        @param (str) ip_id: a string representing the resource id of the IP
        @return: True if json method had success else False
        """
        ip_id = '    "IpAddressResourceId": %s' % ip_id
        json_scheme = self.gen_def_json_scheme('SetRemoveIpAddress', ip_id)
        json_obj = self.call_method_post(method='SetRemoveIpAddress', json_scheme=json_scheme)
        pprint(json_obj)
        return True if json_obj['Success'] is True else False

    def get_package_id(self, name):
        """
        Retrieve the smart package id given is English name
        @param (str) name: the Aruba Smart package size name, ie: "small", "medium", "large", "extra large".
        @return: The package id that depends on the Data center and the size choosen.
        """
        json_scheme = self.gen_def_json_scheme('GetPreConfiguredPackages', dict(HypervisorType=4))
        json_obj = self.call_method_post(method='GetPreConfiguredPackages ', json_scheme=json_scheme)
        for package in json_obj['Value']:
            packageId  = package['PackageID']
            for description in package['Descriptions']:
                languageID = description['LanguageID']
                packageName = description['Text']
                if languageID == 2 and packageName.lower() == name.lower():
                    return packageId

    def get_ip(self):
        """
        Retrieve a complete list of bought ip address related only to PRO Servers.
        It create an internal object (Iplist) representing all of the ips object
        iterated form the WS.
        @param: None
        @return: None
        """
        json_scheme = self.gen_def_json_scheme('GetPurchasedIpAddresses')
        json_obj = self.call_method_post(method='GetPurchasedIpAddresses ', json_scheme=json_scheme)
        self.iplist = IpList()
        for ip in json_obj['Value']:
            r = Ip()
            r.ip_addr = ip['Value']
            r.resid = ip['ResourceId']
            r.serverid = ip['ServerId'] if 'None' not in str(ip['ServerId']) else None
            self.iplist.append(r)

    def delete_vm(self, server=None, server_id=None):
        self.logger.debug('%s: Deleting: %s' % (self.__class__.__name__, server))
        sid = server_id if server_id is not None else server.sid
        self.logger.debug('%s: Deleting SID: %s' % (self.__class__.__name__, sid))
        if sid is None:
            raise Exception('NoServerSpecified')
        json_scheme = self.gen_def_json_scheme('SetEnqueueServerDeletion', dict(ServerId=sid))
        json_obj = self.call_method_post(method='SetEnqueueServerDeletion', json_scheme=json_scheme)
        print('Deletion enqueued successfully for server_id: %s' % sid)
        return True if json_obj['Success'] is 'True' else False

    def get_jobs(self):
        json_scheme = self.gen_def_json_scheme('GetJobs')
        return self.call_method_post(method='GetJobs', json_scheme=json_scheme)

    def find_job(self, vm_name):
        jobs_list = self.get_jobs()
        if jobs_list['Value'] is None:
            _i = 0
            while jobs_list['Value'] is not None:
                _i += 1
                jobs_list = self.get_jobs()
                if _i > 10:
                    return 'JOBNOTFOUND'
        if len(jobs_list['Value']) <= 0:
            return 'JOBNOTFOUND'
        for job in jobs_list['Value']:
            if vm_name in job['ServerName']:
                return job
        return 'JOBNOTFOUND'

    def get_virtual_datacenter(self):
        json_scheme = self.gen_def_json_scheme('GetVirtualDatacenter')
        json_obj = self.call_method_post(method='GetVirtualDatacenter', json_scheme=json_scheme)
        return json_obj

    def get_server_detail(self, server_id):
        json_scheme = self.gen_def_json_scheme('GetServerDetails', dict(ServerId=server_id))
        json_obj = self.call_method_post(method='GetServerDetails', json_scheme=json_scheme)
        return json_obj['Value']

    def attach_vlan(self, network_adapter_id, vlan_resource_id, ip=None, subnet_mask=None, gateway=None):
        if gateway is not None:
            additional_fields = {
                "VLanRequest": {
                    "NetworkAdapterId": network_adapter_id,
                    "SetOnVirtualMachine": "true",
                    "VLanResourceId": vlan_resource_id,
                    "PrivateIps": [{
                        "GateWay": gateway,
                        "IP": ip,
                        "SubNetMask": subnet_mask
                    }]
                }
            }
        else:
            additional_fields = {
                "VLanRequest": {
                    "NetworkAdapterId": network_adapter_id,
                    "SetOnVirtualMachine": "false",
                    "VLanResourceId": vlan_resource_id,
                    "PrivateIps": [{
                        "GateWay": None,
                        "IP": None,
                        "SubNetMask": None
                    }]
                }
            }
        json_scheme = self.gen_def_json_scheme('SetEnqueueAssociateVLan', method_fields=additional_fields)
        json_obj = self.call_method_post(method='SetEnqueueAssociateVLan', json_scheme=json_scheme)
        return True if json_obj['Success'] is True else False

    def detach_vlan(self, network_adapter_id, vlan_resource_id):
        vlan_request = {
            "VLanRequest": {
                "NetworkAdapterId": network_adapter_id,
                "SetOnVirtualMachine": "false",
                "VLanResourceId": vlan_resource_id
            }
        }
        json_scheme = self.gen_def_json_scheme('SetEnqueueDeassociateVLan', method_fields=vlan_request)
        json_obj = self.call_method_post(method='SetEnqueueDeassociateVLan', json_scheme=json_scheme)
        return True if json_obj['Success'] is True else False

    def create_snapshot(self, dc, server_id=None):
        sid = CloudInterface(dc).get_server_detail(server_id)
        if sid['HypervisorType'] is not 4:
            snapshot_request = {
                "Snapshot": {
                    "ServerId": server_id,
                    "SnapshotOperationTypes": "Create"
                }
            }
            json_scheme = self.gen_def_json_scheme('SetEnqueueServerSnapshot', method_fields=snapshot_request)
            json_obj = self.call_method_post(method='SetEnqueueServerSnapshot', json_scheme=json_scheme)
            return True if json_obj['Success'] is True else False

    def restore_snapshot(self, server_id=None):
        snapshot_request = {
            "Snapshot": {
                "ServerId": server_id,
                "SnapshotOperationTypes": "Restore"
            }
        }
        json_scheme = self.gen_def_json_scheme('SetEnqueueServerSnapshot', method_fields=snapshot_request)
        json_obj = self.call_method_post(method='SetEnqueueServerSnapshot', json_scheme=json_scheme)
        return True if json_obj['Success'] is True else False

    def delete_snapshot(self, server_id=None):
        snapshot_request = {
            "Snapshot": {
                "ServerId": server_id,
                "SnapshotOperationTypes": "Delete"
            }
        }
        json_scheme = self.gen_def_json_scheme('SetEnqueueServerSnapshot', method_fields=snapshot_request)
        json_obj = self.call_method_post(method='SetEnqueueServerSnapshot', json_scheme=json_scheme)
        return True if json_obj['Success'] is True else False

    def archive_vm(self, dc, server_id=None):
        sid = CloudInterface(dc).get_server_detail(server_id)
        if sid['HypervisorType'] is not 4:
            archive_request = {
                "ArchiveVirtualServer": {
                    "ServerId": server_id
                }
            }
            json_scheme = self.gen_def_json_scheme('ArchiveVirtualServer', method_fields=archive_request)
            json_obj = self.call_method_post(method='ArchiveVirtualServer', json_scheme=json_scheme)
            return True if json_obj['Success'] is True else False

    def restore_vm(self, server_id=None, cpu_qty=None, ram_qty=None):
        restore_request = {
            "Server": {
                "ServerId": server_id,
                "CPUQuantity": cpu_qty,
                "RAMQuantity": ram_qty
            }
        }
        json_scheme = self.gen_def_json_scheme('SetEnqueueServerRestore', method_fields=restore_request)
        json_obj = self.call_method_post(method='SetEnqueueServerRestore', json_scheme=json_scheme)
        return True if json_obj['Success'] is True else False
