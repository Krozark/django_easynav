# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-easynav',
    version='0.1.0',
    description='a module that allows you to manage the navigation, but also create generic pages stored entirely in the database for Django',
    author='Maxime Barbier',
    author_email='maxime.barbier1991@gmail.com',
    url='https://github.com/Krozark/django_easynav',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
