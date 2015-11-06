from distutils.core import setup

setup(
    name='pyArubaCloud',
    version='0.6',
    packages=['ArubaCloud', 'ArubaCloud.base', 'ArubaCloud.helper', 'ArubaCloud.objects',
              'ArubaCloud.objects.VmTypes', 'ArubaCloud.PyArubaAPI'],
    url='https://github.com/ArubaCloud/pyArubaCloud/',
    license='Apache',
    author='Alessio Rocchi',
    author_email='labs@arubacloud.com',
    description='Python Interface for Aruba Cloud IaaS'
)
