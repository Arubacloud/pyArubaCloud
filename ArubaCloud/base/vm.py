class VMList(list):
    def __init__(self, *args, **kwargs):
        super(VMList, self).__init__(*args)
        self.last_search_result = []

    def find(self, name):
        """
        Return a list of subset of VM that match the pattern name
        @param name (str): the vm name of the virtual machine
        @param name (Obj): the vm object that represent the virtual
                           machine (can be Pro or Smart)
        @return (list): the subset containing the serach result.
        """
        if name.__class__ is 'base.Server.Pro' or name.__class__ is 'base.Server.Smart':
            # print('DEBUG: matched VM object %s' % name.__class__)
            pattern = name.vm_name
        else:
            # print('DEBUG: matched Str Object %s' % name.__class__)
            pattern = name
        # 14/06/2013: since this method is called within a thread and I wont to pass the return objects with queue or
        # call back, I will allocate a list inside the Interface class object itself, which contain all of the vm found
        # 02/11/2015: this must be changed ASAP! it's a mess this way... what was I thinking??
        self.last_search_result = [vm for vm in self if pattern in vm.vm_name]
        return self.last_search_result

    def show(self):
        for vm in self:
            print(vm)

    def find_ip(self, ip):
        f = None
        if ip.__class__ is 'base.Ip.Ip':
            # logger.debug('DEBUG: matched IP Object: %s' % ip.__class__)
            pattern = ip.ip_addr
        else:
            # logger.debug('DEBUG: matched Str Object: %s' % ip.__class__)
            pattern = ip
        for vm in self:
            if vm.__class__.__name__ is 'Smart':
                if pattern == vm.ip_addr:
                    f = vm
            else:
                if pattern == vm.ip_addr.ip_addr:
                    f = vm
        return f


class VM(object):
    vm_name = None
    cpu_qty = None
    ram_qty = None
    status = None
    sid = None
    datacenter_id = None
    auth = None
    admin_password = None
    wcf_baseurl = None
    template_id = None
    hd_total_size = None
    hd_qty = None

    def __init__(self, interface):
        super(VM, self).__init__()
        self.interface = interface

    def poweroff(self, debug=False):
        data = dict(
            ServerId=self.sid
        )
        json_scheme = self.interface.gen_def_json_scheme('SetEnqueueServerPowerOff', data)
        json_obj = self.interface.call_method_post('SetEnqueueServerPowerOff', json_scheme=json_scheme, debug=debug)
        return True if json_obj['Success'] is True else False

    def poweron(self, debug=False):
        data = dict(
            ServerId=self.sid
        )
        json_scheme = self.interface.gen_def_json_scheme('SetEnqueueServerStart', data)
        json_obj = self.interface.call_method_post('SetEnqueueServerStart', json_scheme=json_scheme, debug=debug)
        return True if json_obj['Success'] is 'True' else False

    def reinitialize(self, admin_password=None, debug=False, ConfigureIPv6=False, OSTemplateID=None):
        """
        Reinitialize a VM.
        :param admin_password: Administrator password.
        :param debug: Flag to enable debug output.
        :param ConfigureIPv6: Flag to enable IPv6 on the VM.
        :param OSTemplateID: TemplateID to reinitialize the VM with.
        :return: True in case of success, otherwise False
        :type admin_password: str
        :type debug: bool
        :type ConfigureIPv6: bool
        :type OSTemplateID: int
        """
        data = dict(
            AdministratorPassword=admin_password,
            ServerId=self.sid,
            ConfigureIPv6=ConfigureIPv6
        )
        if OSTemplateID is not None:
            data.update(OSTemplateID=OSTemplateID)
        assert data['AdministratorPassword'] is not None, 'Error reinitializing VM: no admin password specified.'
        assert data['ServerId'] is not None, 'Error reinitializing VM: no Server Id specified.'
        json_scheme = self.interface.gen_def_json_scheme('SetEnqueueReinitializeServer', method_fields=data)
        json_obj = self.interface.call_method_post('SetEnqueueReinitializeServer', json_scheme=json_scheme, debug=debug)
        return True if json_obj['Success'] is 'True' else False

    def edit_cpu(self, cpu_qty, debug=False):
        raise NotImplemented()

    def edit_ram(self, ram_qty, debug=False):
        raise NotImplemented()

    def add_virtual_disk(self, *args, **kwargs):
        raise NotImplemented()

    def remove_virtual_disk(self, *args, **kwargs):
        raise NotImplemented()

    def edit_virtual_disk_size(self, *args, **kwargs):
        raise NotImplemented()
