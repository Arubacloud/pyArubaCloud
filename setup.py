import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pyArubaCloud",
    version="0.7.12",
    author="Aruba S.p.A.",
    author_email="luca.lasagni@staff.aruba.it",
    description="Python Interface to interact with ArubaCloud IaaS Service.",
    license=" Apache License, Version 2.0",
    keywords="arubacloud.com cloud.it Cloud IaaS Api",
    url="https://github.com/Arubacloud/pyArubaCloud",
    packages=['ArubaCloud', 'ArubaCloud.base', 'ArubaCloud.helper', 'ArubaCloud.objects.VmTypes', 'ArubaCloud.objects', 'ArubaCloud.ReverseDns', 'ArubaCloud.ReverseDns.Requests'],
    long_description="Python Interface to interact with ArubaCLoud IaaS Service.",
    classifiers=[
        "Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: Information Technology",
		"Intended Audience :: System Administrators",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.6",
		"Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    install_requires=['requests>=2.4.2', 'jsonpickle']
)
