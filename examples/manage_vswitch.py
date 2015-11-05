import argparse

from ArubaCloud.PyArubaAPI import CloudInterface

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datacenter', help='Specify datacenter to login.', action='store', dest='dc')
    parser.add_argument('-u', '--username', help='Specify username.', action='store', dest='username')
    parser.add_argument('-w', '--password', help='Specify password.', action='store', dest='password')
    parser.add_argument('-t', '--template', help='Specify template.', action='store', dest='template')
    parser.add_argument('--vlan-name', help='Specify vSwitch Name.', action='store', dest='vlan_name')
    parser.add_argument('--vm-name', help='Name of the VM to attach the new VLAN.', action='store', dest='vm_name')
    p = parser.parse_args()

    i = CloudInterface(dc=p.dc)
    i.login(username=p.username, password=p.password, load=True)

    # create new vlan (virtual switch)
    vlan = i.purchase_vlan(p.vlan_name)

    # find the vm object
    vm = i.vmlist.find(p.vm_name)[0]
    # find the network adapter object
    network_adapter = i.get_server_detail(server_id=vm.sid)['NetworkAdapters'][1]
    # attach the network adapter to the created vlan
    i.attach_vlan(network_adapter_id=network_adapter['Id'], vlan_resource_id=vlan.resource_id)

    # retrieve every vlan in the datacenter and remove them
    raw_input(
        "You are going to delete every VLAN in Datacenter: {}, press any key to continue (CTRL+C to abort)".format(
            p.dc
        )
    )
    vlans = i.get_vlan()
    for vlan in vlans:
        i.remove_vlan(vlan.resource_id)
