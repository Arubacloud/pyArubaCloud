import argparse
import time

from ArubaCloud.PyArubaAPI import CloudInterface

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

    maxretries = 5
    for vm in i.vmlist.find(name=p.pattern):
        if vm.status == 3:
            vm.poweroff()
        for w in range(maxretries):
            server_detail = i.get_server_detail(server_id=vm.sid)
            if server_detail['ServerStatus'] == 2:
                break
            else:
                print("Waiting shutdown")
                time.sleep(5)
        
        i.delete_vm(server_id=vm.sid)