import argparse
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
    parser.add_argument('--pkg', help='Specify package: [small|medium|large|extralarge]', action='store',
                        dest='pkg', default='small')
    p = parser.parse_args()

    i = CloudInterface(dc=p.dc)
    i.login(username=p.username, password=p.password, load=True)

    from ArubaCloud.objects import SmartVmCreator
    c = SmartVmCreator(name=p.vmname, admin_password=p.vmpassword, template_id=p.template, auth_obj=i.auth)
    c.set_type(size=p.pkg)

    pprint(c.get_json())

    print(c.commit(url=i.wcf_baseurl, debug=True))
