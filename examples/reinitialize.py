import argparse
import time

from ArubaCloud.PyArubaAPI import CloudInterface

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datacenter', help='Specify datacenter to login.', action='store', type=int, dest='dc')
    parser.add_argument('-p', '--pattern', help='Specify pattern to search.', action='store', dest='pattern')
    parser.add_argument('-u', '--username', help='Specify username.', action='store', dest='username')
    parser.add_argument('-w', '--password', help='Specify password.', action='store', dest='password')
    parser.add_argument('--new-admin-password', action='store', dest='new_admin_passwd')
    p = parser.parse_args()

    o = CloudInterface(p.dc)
    o.login(p.username, p.password, False)
    for vm in o.get_vm(pattern=p.pattern):
        print('Reinitialize: %s' % vm.vm_name)
        vm.poweroff()
        while len(o.get_jobs()['Value']) > 0:
            time.sleep(1)
        vm.reinitialize(admin_password=p.new_admin_passwd)
