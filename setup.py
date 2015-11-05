from setuptools import setup

setup(
    name='pyArubaCloud',
    version='0.6',
    packages=['examples', 'ArubaCloud', 'ArubaCloud.base', 'ArubaCloud.tools', 'ArubaCloud.helper',
              'ArubaCloud.objects', 'ArubaCloud.objects.VmTypes'],
    url='http://www.github.com/ArubaCloud/pyArubaCloud',
    license='GPL',
    author='Alessio Rocchi',
    author_email='alessio.rocchi@staff.aruba.it',
    description='Python Library to interact with Aruba Cloud IaaS', requires=['requests']
)
