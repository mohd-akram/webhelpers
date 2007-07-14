from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(
    name="WebHelpers",
    version='0.3.1',
    description='Web Helpers',
    long_description="""
Web Helpers is a library of helper functions intended to make writing templates in web
applications easier. 

One of the sub-sections of Web Helpers contains a full port of the template helpers that
are provided by Ruby on Rails with slight adaptations on occasion to accomodate for Python.

Some of these helpers only require `Routes <http://routes.groovie.org/>`_ to function.

* `Development svn <http://pylonshq.com/svn/WebHelpers/trunk#egg=WebHelpers-dev>`_

""",
    author='Ben Bangert, Phil Jenvey',
    author_email='ben@groovie.org, pjenvey@groovie.org',
    url='http://pylonshq.com/WebHelpers/',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "Routes>=1.7", "simplejson>=1.4",
        ],
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: BSD License",
                 "Programming Language :: Python",
                 "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                 "Topic :: Software Development :: Libraries :: Python Modules",
               ],
    entry_points="""
    [buildutils.optional_commands]
    compress_resources = webhelpers.commands
    """,
)
