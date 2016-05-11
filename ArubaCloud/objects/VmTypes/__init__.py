from ArubaCloud.base.Errors import OperationNotPermitted, MalformedJsonRequest
from ArubaCloud.base.vm import VM
from ArubaCloud.objects import Ip
from ArubaCloud.objects import VirtualDiskOperation


class Smart(VM):
    def __init__(self, interface, sid):
        super(Smart, self).__init__(interface)
        self.cltype = 'smart'
        self.sid = sid
        self.ip_addr = Ip()
        self.package = None

    def __str__(self):
        msg = super(Smart, self).__str__()
        msg += ' -> IPAddr: %s\n' % self.ip_addr
        return msg

    def upgrade_vm(self, package_id, debug=False):
        if not self.status == 2:
            raise OperationNotPermitted("Cannot edit resources in the current state of the VM. Turn off the VM first.")
        if package_id > 4 or package_id <= 0:
            return MalformedJsonRequest("Packages available are: 1, 2, 3, 4.")
        method_json = {
            "Server": {
                "ServerId": self.sid,
                "SmartVMWarePackageID": package_id
            }
        }
        json_obj = self.interface.call_method_post(method='SetEnqueueServerUpdate',
                                                   json_scheme=self.interface.gen_def_json_scheme(
                                                       req='SetEnqueueServerUpdate',
                                                       method_fields=method_json
                                                   ),
                                                   debug=debug)
        if debug is True:
            print(json_obj)
        return True if json_obj['Success'] is True else False


class Pro(VM):
    def __init__(self, interface, sid):
        super(Pro, self).__init__(interface)
        self.cltype = 'pro'
        self.sid = sid
        self.ip_addr = Ip()
        # Load HD information
        self.hds = []
        _hds = self.interface.get_server_detail(self.sid)['VirtualDisks']
        for hd in _hds:
            self.hds.append(hd)

    """
    Methods specific for Pro VM
    """

    def _commit_compute_resources(self):
        method_json = {
            "ServerId": self.sid,
            "CpuQuantity": self.cpu_qty,
            "RamQuantity": self.ram_qty,
            "RestartAfterExecuted": 'true'
        }
        json_obj = self.interface.call_method_post(method='SetEnqueueHardwareUpdate',
                                                   json_scheme=self.interface.gen_def_json_scheme(
                                                       req='SetEnqueueHardwareUpdate',
                                                       method_fields=method_json)
                                                   )
        return json_obj

    def edit_cpu(self, cpu_qty, debug=False):
        if not self.status == 2:
            raise OperationNotPermitted("Cannot edit resources in the current state of the VM.")
        self.cpu_qty = cpu_qty
        json_obj = self._commit_compute_resources()
        if debug is True:
            print(json_obj)
        return True if json_obj['Success'] is True else False

    def edit_ram(self, ram_qty, debug=False):
        if not self.status == 2:
            raise OperationNotPermitted("Cannot edit resources in the current state of the VM.")
        self.ram_qty = ram_qty
        json_obj = self._commit_compute_resources()
        if debug is True:
            print(json_obj)
        return True if json_obj['Success'] is True else False

    def add_virtual_disk(self, size, debug=False):
        if not self.status == 2:
            raise OperationNotPermitted("Cannot edit resources in the current state of the VM.")
        if len(self.hds) > 3:
            raise ValueError("Cannot create more than 3 disks per VM.")
        virtual_disk_operation = VirtualDiskOperation

        method_json = {
            'ServerId': self.sid,
            'Disk': {
                'CustomVirtualDiskPath': None,
                'Size': size,
                'VirtualDiskType': len(self.hds),  # increment the counter of current present disks
                'VirtualDiskUpdateType': virtual_disk_operation.create
            }
        }
        json_obj = self.interface.call_method_post(method='SetEnqueueVirtualDiskManage',
                                                   json_scheme=self.interface.gen_def_json_scheme(
                                                       req='SetEnqueueVirtualDiskManage',
                                                       method_fields=method_json)
                                                   )
        if debug is True:
            print(json_obj)
        return True if json_obj['Success'] is True else False

    def resize_virtual_disk(self, size, debug=False):
            if not self.status == 2:
                raise OperationNotPermitted("Cannot edit resources in the current state of the VM.")
            if self.hd_total_size > size:
                raise OperationNotPermitted("Cannot decrease size of the disk")
            virtual_disk_operation = VirtualDiskOperation

            method_json = {
                'ServerId': self.sid,
                'Disk': {
                    'CustomVirtualDiskPath': None,
                    'Size': size,
                    'VirtualDiskType': self.hds,
                    'VirtualDiskUpdateType': virtual_disk_operation.resize
                }
            }
            json_obj = self.interface.call_method_post(method='SetEnqueueVirtualDiskManage',
                                                       json_scheme=self.interface.gen_def_json_scheme(
                                                           req='SetEnqueueVirtualDiskManage',
                                                           method_fields=method_json)
                                                       )
            if debug is True:
                print(json_obj)
            return True if json_obj['Success'] is True else False

    def remove_virtual_disk(self, virtual_disk_id, debug=False):
        if not self.status == 2:
            raise OperationNotPermitted("Cannot edit resources in the current state of the VM.")
        virtual_disk_operation = VirtualDiskOperation

        method_json = {
            'ServerId': self.sid,
            'Disk': {
                'CustomVirtualDiskPath': None,
                'Size': 0,
                'VirtualDiskType': virtual_disk_id,
                'VirtualDiskUpdateType': virtual_disk_operation.delete
            }
        }
        json_obj = self.interface.call_method_post(method='SetEnqueueVirtualDiskManage',
                                                   json_scheme=self.interface.gen_def_json_scheme(
                                                       req='SetEnqueueVirtualDiskManage',
                                                       method_fields=method_json)
                                                   )
        if debug is True:
            print(json_obj)
        return True if json_obj['Success'] is True else False

    def __str__(self):
        msg = super(Pro, self).__str__()
        msg += ' -> IPAddr: %s\n' % self.ip_addr
        return msg
