Python Interface for ArubaCloud IaaS Service. This is an early-stage release, not every features has been covered.

This project is under development, the classes, methods and parameters might change over time. This README usually reflects the syntax of the latest version.

#Getting Started
##Installation
```
git clone https://github.com/Arubacloud/pyArubaCloud.git pyArubaCloud
cd pyArubaCloud
python setup.py install
```

##Usage
In the examples folder you can find some examples about various operations which can be done via API.

###Login into service
```
from ArubaCloud.PyArubaAPI import CloudInterface

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)
```
Once you have instantiate CloudInterface object specifing the number of the datacenter(1 to 6), keeping in mind this association:
- 1 -> DC1 -> Italy
- 2 -> DC2 -> Italy
- 3 -> DC3 -> Czech Republic
- 4 -> DC4 -> France
- 5 -> DC5 -> Germany
- 6 -> DC6 -> UK

You can login with your username and password (i.e. AWI-19054), `load` parameter is used to cache all of the data related to the account (within the datacenter) at login fase.

###Retrieve all templates related to an hypervisor
You have 4 types of hypervisors to choose, here the lists of them:
- 1 -> Microsoft Hyper-V - Cloud Pro
- 2 -> VMWare - Cloud Pro
- 3 -> Microsoft Hyper-V Low Cost - Cloud Pro
- 4 -> VMWare - Cloud Smart

Assuming that we want to list every template that contains Debian in the Description for the hypervisor 4 in Datacenter 2, the code is the following:
```
from ArubaCloud.PyArubaAPI import CloudInterface

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)
ci.get_hypervisors()

from pprint import pprint
pprint(ci.find_template(name='Debian', hv=4))
```

### Create a new VM
In order to create a VM you have to instantiate the specific object exposed from ArubaCloud.objects package:
- ProVmCreator
- SmartVmCreator

About Pro VMs, you can choose an high number of customizations, such as, cpu number, ram quantity, number and size of virtual disks, public IPs, private IPs and so on.

Smart Servers are not customizable (this reflect the behaviour of the service itself), but you can choose 4 different size:
- Small
- Medium
- Large
- Extra Large

#### Example to create a Pro VM
```
from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.objects import ProVmCreator

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)

ip = i.purchase_ip()

c = ProVmCreator(name='debian01', admin_password='MyStrongPassword', template_id='1761', auth_obj=ci.auth)
c.set_cpu_qty(2)
c.set_ram_qty(6)
  
c.add_public_ip(public_ip_address_resource_id=ip.resid)
c.add_virtual_disk(20)
c.add_virtual_disk(40)

print(c.commit(url=ci.wcf_baseurl, debug=True))
```

#### Example to create a Smart VM
```
from ArubaCloud.PyArubaAPI import CloudInterface
from ArubaCloud.objects import SmartVmCreator

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)

c = SmartVmCreator(name='small01', admin_password='MyStrongPassword', template_id=761, auth_obj=ci.auth)
c.set_type(size='small')

print(c.commit(url=ci.wcf_baseurl, debug=True))
```

For more examples, check [this link](https://github.com/Arubacloud/pyArubaCloud/tree/master/examples)
