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

    poweroff_check = 0
    maxretries = 5
    sleep_for = 5
    attempts = 0
    for vm in i.vmlist.find(name=p.pattern):
        if vm.status == 3:
            print('Turn off VM: %s' % vm.vm_name)
            vm.poweroff()
            poweroff_check = 1
            time.sleep(sleep_for)
            for w in range(maxretries):
                attempts += 1
                server_detail = i.get_server_detail(server_id=vm.sid)
                if server_detail['ServerStatus'] == 2:
                    break
                else:
                    print('Waiting shutdown for other %s seconds' % sleep_for)
                    time.sleep(sleep_for)

        if attempts < maxretries:
            if poweroff_check == 0:
                print('VM %s is already Off. Starting...' % vm.vm_name)
            else:
                print('Restarting VM %s' % vm.vm_name)
            attempts = 0
            vm.poweron()
            time.sleep(sleep_for)
            for w in range(maxretries):
                attempts += 1
                server_detail = i.get_server_detail(server_id=vm.sid)
                if server_detail['ServerStatus'] == 3:
                    break
                else:
                    print('Waiting power on for other %s seconds' % sleep_for)
                    time.sleep(sleep_for)

            if attempts < maxretries:
                print('Restart VM %s complete.' % vm.vm_name)
            else:
                print('Time out! Too many attempts during VM %s Turning On.' % vm.vm_name)

        else:
            print('Time out! Too many attempts during VM %s Shutting down.' % vm.vm_name)