# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="requestions",
    version="0.0.1",
    url="https://github.com/kanzure/python-requestions",
    license="BSD",
    author="Bryan Bishop",
    author_email="kanzure@gmail.com",
    description="Serialization for Requests using JSON.",
    long_description=open("README.md", "r").read(),
    packages=["requestions"],
    zip_safe=False,
    include_package_data=True,
    install_requires=["requests>=0.14.2"],
    platforms="any",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        'Natural Language :: English',
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        #"Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
    ]
)
