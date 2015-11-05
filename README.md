Python Interface for ArubaCloud IaaS Service. This is an early-stage release, not every features are been covered.

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

You can now login with your username and password (i.e. AWI-19054), the parameter `load` is used to load all of the data related to the account (within the datacenter) at login fase.

###Retrieve all templates related to an hypervisor
You have 4 types of hypervisors to choose, here the lists of them:
- 1 -> Microsoft Hyper-V - Cloud Pro
- 2 -> VMWare - Cloud Pro
- 3 -> Microsoft Hyper-V Low Cost - Cloud Pro
- 4 -> VMWare - Cloud Smart
Assuming that, we want to list every template that contains Debian in the Description for the hypervisor 4 in Datacenter 2, the code is the following:
```
from ArubaCloud.PyArubaAPI import CloudInterface

ci = CloudInterface(dc=1)
ci.login(username="XXX-XXXX", password="XXXXXXXX", load=True)
ci.get_hypervisors()

from pprint import pprint
pprint(ci.find_template(name='Debian', hv=4))
```
For more examples, check [this link](https://github.com/Arubacloud/pyArubaCloud/tree/master/examples)
