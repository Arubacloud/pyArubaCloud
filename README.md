[![Code Climate](https://codeclimate.com/github/Arubacloud/pyArubaCloud/badges/gpa.svg)](https://codeclimate.com/github/Arubacloud/pyArubaCloud)

Python Interface for ArubaCloud IaaS Service. This is an early-stage release, not every features has been covered.

This project is under development, the classes, methods and parameters might change over time. This README usually reflects the syntax of the latest version.

# Getting Started
## Installation
Python Package:
```
pip install pyarubacloud
```

Git Version:
```
git clone https://github.com/Arubacloud/pyArubaCloud.git pyArubaCloud
cd pyArubaCloud
python setup.py install
```

## Usage
In the examples folder you can find some examples on various operations which can be done via API.

### Log in to the service
``` python
from ArubaCloud.PyArubaAPI import CloudInterface

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)
```
Once you have instantiated CloudInterface object by specifying the number of the datacenter(1 to 6), keeping in mind this association:
- 1 -> DC1 -> Italy
- 2 -> DC2 -> Italy
- 3 -> DC3 -> Czech Republic
- 4 -> DC4 -> France
- 5 -> DC5 -> Germany
- 6 -> DC6 -> UK

You can login with your username and password (i.e. AWI-19054), `load` parameter is used to cache all of the data related to the account (within the datacenter) at the login phase.

### Retrieve all templates related to a hypervisor
You have the following 4 types of hypervisors to choose from:
- 1 -> Microsoft Hyper-V - Cloud Pro
- 2 -> VMWare - Cloud Pro
- 3 -> Microsoft Hyper-V Low Cost - Cloud Pro
- 4 -> VMWare - Cloud Smart

Assuming that we want to list every template that contains Debian in the Description for hypervisor 4 in Datacenter 2, the code will be the following:
``` python
from ArubaCloud.PyArubaAPI import CloudInterface

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)
ci.get_hypervisors()

from pprint import pprint
pprint(ci.find_template(name='Debian', hv=4))
```
When you select a template to create a new machine the template has to be enabled. In the result of find_template you can check if a template is enabled.
```
[Template Name: Debian 5 32bit, Hypervisor: SMART, Id: 959, Enabled: False,
 Template Name: Debian 5 64bit, Hypervisor: SMART, Id: 960, Enabled: False,
 Template Name: Debian 6 32bit, Hypervisor: SMART, Id: 961, Enabled: False,
 Template Name: Debian 6 64bit, Hypervisor: SMART, Id: 962, Enabled: False,
 Template Name: Debian 7 64bit, Hypervisor: SMART, Id: 1114, Enabled: True,
 Template Name: Debian 7 32bit, Hypervisor: SMART, Id: 1115, Enabled: True,
 Template Name: Debian 8 64bit, Hypervisor: SMART, Id: 1723, Enabled: True]
```
### Create a new VM
In order to create a VM you have to instantiate the specific object exposed by the ArubaCloud.objects package:
- ProVmCreator
- SmartVmCreator

About Pro VMs, you can choose from a large number of customizations, such as, number of cpu, ram quantity, number and size of virtual disks, public IPs, private IPs and so on.

Smart Servers are not customizable (this reflects the behaviour of the service itself), but you can choose 4 different sizes:
- Small
- Medium
- Large
- Extra Large

#### Example of how to create a Pro VM
``` python
from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.objects import ProVmCreator

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)

ip = ci.purchase_ip()

# template_id: 1605 [Template Name: CentOS 7.x 64bit, Hypervisor: VW, Id: 1605, Enabled: True]
c = ProVmCreator(name='debian01', admin_password='MyStrongPassword', template_id='1605', auth_obj=ci.auth)
c.set_cpu_qty(2)
c.set_ram_qty(6)
  
c.add_public_ip(public_ip_address_resource_id=ip.resid)
c.add_virtual_disk(20)
c.add_virtual_disk(40)

print(c.commit(url=ci.wcf_baseurl, debug=True))
```

#### Example of how to create a Smart VM
``` python
from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.objects import SmartVmCreator

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)

# template_id: 1114 [Hypervisor: SMART (Debian 7 - 64bit)]
c = SmartVmCreator(name='small01', admin_password='MyStrongPassword', template_id=1114, auth_obj=ci.auth)
c.set_type(ci.get_package_id('small'))

print(c.commit(url=ci.wcf_baseurl, debug=True))
```

#### Example of how to set a SSH key
``` python
c.set_ssh_key('your_public_key.pub')
```

#### Example to use ReverseDns
``` python
from ArubaCloud.ReverseDns import ReverseDns

ci = CloudInterface(dc=1)
rdns = ReverseDns(username='XXX-XXXX', password='XXXXXXX', ws_uri=ci.wcf_baseurl)

# get configured reverse dns
print(rdns.get())

# set a new reverse dns with one or more PTR hosts
print(rdns.set(address='XXX.XXX.XXX.XXX', host_name=['rhost1', 'rhost2']

# reset a reverse dns
print(rdns.reset(address='XXX.XXX.XXX.XXX')

```

More examples can be found in the [examples folder](https://github.com/Arubacloud/pyArubaCloud/tree/master/examples), following the complete list:
- [Delete a VM](https://github.com/Arubacloud/pyArubaCloud/blob/master/examples/delete_vm.py)
- [Edit Pro VM Hardware](https://github.com/Arubacloud/pyArubaCloud/blob/master/examples/edit_vm_hardware.py)
- [Manage VLAN (add, attach, deattach, remove)](https://github.com/Arubacloud/pyArubaCloud/blob/master/examples/manage_vswitch.py)
- [Reinitialize Smart VM](https://github.com/Arubacloud/pyArubaCloud/blob/master/examples/reinitialize.py)
