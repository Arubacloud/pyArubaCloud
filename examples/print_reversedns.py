import argparse

from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.ReverseDns import ReverseDns
from ArubaCloud.objects.VmTypes import Smart, Pro

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datacenter', help='Specify datacenter to login.', action='store', type=int, dest='dc')
    parser.add_argument('-u', '--username', help='Specify username.', action='store', dest='username')
    parser.add_argument('-w', '--password', help='Specify password.', action='store', dest='password')
    p = parser.parse_args()

    ci = CloudInterface(dc=p.dc)
    ci.login(username=p.username, password=p.password, load=True)
    ci.get_servers()
    rdns = ReverseDns.ReverseDns(username=p.username, password=p.password, ws_uri=ci.wcf_baseurl)

    for vm in ci.vmlist:
        print("---")
        print("VM Name: {}".format(vm.vm_name))
        print("VM Type: {}".format(type(vm)))        
        if isinstance(vm, Smart):
            print(rdns.get(addresses=[vm.ip_addr]))
        elif isinstance(vm, Pro):
            for ip in vm.ip_addr:
                print(rdns.get(addresses=[ip.ip_addr]))
                

    # get configured reverse dns
