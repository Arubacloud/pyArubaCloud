import argparse

from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.objects.VmTypes import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datacenter', help='Specify datacenter to login.', action='store', type=int, dest='dc')
    parser.add_argument('-p', '--pattern', help='Specify pattern to search.', action='store', dest='pattern')
    parser.add_argument('-u', '--username', help='Specify username.', action='store', dest='username')
    parser.add_argument('-w', '--password', help='Specify password.', action='store', dest='password')
    p = parser.parse_args()

    i = CloudInterface(dc=p.dc)
    i.login(username=p.username, password=p.password, load=True)

    i.get_servers()

    for vm in i.vmlist:
        print("VM Name: {}".format(vm.vm_name))
        print("VM Type: {}".format(type(vm)))
        if isinstance(vm, Smart):
            print("VM IP: {}".format(vm.ip_addr))
        elif isinstance(vm, Pro):
            print("VM IP: {}".format(vm.ip_addr.ip_addr))
        print("############################")
