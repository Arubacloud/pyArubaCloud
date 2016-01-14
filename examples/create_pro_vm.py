import argparse
import logging
from pprint import pprint

from ArubaCloud.PyArubaAPI import CloudInterface

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datacenter', help='Specify datacenter to login.', action='store', dest='dc')
    parser.add_argument('-u', '--username', help='Specify username.', action='store', dest='username')
    parser.add_argument('-w', '--password', help='Specify password.', action='store', dest='password')
    parser.add_argument('-t', '--template', help='Specify template.', action='store', dest='template')
    parser.add_argument('-n', '--name', help='Specify VM name', action='store', dest='vmname')
    parser.add_argument('--vmpassword', help='Specify VM admin password.', action='store', dest='vmpassword',
                        default='ArubaCloud2015')
    p = parser.parse_args()

    i = CloudInterface(dc=p.dc, debug_level=logging.DEBUG)
    i.login(username=p.username, password=p.password, load=False)

    ip = i.purchase_ip(debug=True)
    from ArubaCloud.objects import ProVmCreator

    c = ProVmCreator(name=p.vmname, admin_password=p.vmpassword, template_id=p.template, auth_obj=i.auth)
    c.set_cpu_qty(2)
    c.set_ram_qty(6)
    c.add_public_ip(public_ip_address_resource_id=ip.resid)
    c.add_virtual_disk(20)
    c.add_virtual_disk(40)

    pprint(c.get_json())

    print(c.commit(url=i.wcf_baseurl, debug=True))
