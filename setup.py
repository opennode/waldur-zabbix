#!/usr/bin/env python
from setuptools import setup, find_packages


dev_requires = [
    'Sphinx==1.2.2',
]

tests_require = [
    'factory_boy==2.4.1',
    'django-celery==3.1.16',
    'mock==1.0.1',
    'mock-django==0.6.6',
    'six>=1.9.0',
]

install_requires = [
    'waldur-core>=0.151.0',
    'pyzabbix>=0.7.2',
]


setup(
    name='waldur-zabbix',
    version='0.8.1',
    author='OpenNode Team',
    author_email='info@opennodecloud.com',
    url='http://waldur.com',
    description='Waldur Zabbix adds support for Zabbix monitoring server management',
    license='MIT',
    long_description=open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_requires,
    zip_safe=False,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'waldur_extensions': (
            'waldur_zabbix = waldur_zabbix.extension:ZabbixExtension',
        ),
    },
    # tests_require=tests_requires,
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
