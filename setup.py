import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pyArubaCloud",
    version="0.7",
    author="Alessio Rocchi",
    author_email="alessio.rocchi@staff.aruba.it",
    description="Python Interface to interact with ArubaCloud IaaS Service.",
    license="MIT",
    keywords="arubacloud",
    url="https://github.com/Arubacloud/pyArubaCloud",
    packages=['ArubaCloud', 'ArubaCloud.base', 'ArubaCloud.helper', 'ArubaCloud.objects.VmTypes', 'ArubaCloud.objects'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=['requests>=2.1.9']
)
