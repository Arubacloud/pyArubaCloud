import argparse

from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.objects import VirtualDisk

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datacenter', help='Specify datacenter to login.', action='store', dest='dc')
    parser.add_argument('-p', '--pattern', help='Specify pattern to search.', action='store', dest='pattern')
    parser.add_argument('-u', '--username', help='Specify username.', action='store', dest='username')
    parser.add_argument('-w', '--password', help='Specify password.', action='store', dest='password')
    parser.add_argument('--vm_name', help='Specify VM Name.', action='store', dest='vm_name')

    i = CloudInterface(dc='2')
    i.login(username=p.username, password=p.password, load=True)

    vm = i.find_vm(pattern=p.vm_name)[0]
    # vm.poweroff()

    # Set the amount of CPU cores
    # vm.edit_cpu(cpu_qty=1, debug=True)

    # Set the amount of RAM GB
    # vm.edit_ram(ram_qty=2, debug=True)

    # Add a new Virtual Disk
    # vm.add_virtual_disk(size=10)

    # Delete a Virtual Disk
    vm.remove_virtual_disk(virtual_disk_id=VirtualDisk.additional_disk2_id)


