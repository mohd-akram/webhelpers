from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(
    name="WebHelpers",
    version='0.1',
    description='Web Helpers',
    long_description="""
Rails Helpers is a library of helper functions intended to make writing templates in web
applications easier. As the name indicates, these helpers have been directly ported from
the Ruby on Rails version with slight adaptations on occasion to accomodate for Python.

These helpers only require `Routes <http://routes.groovie.org/>`_ to function.

* `Development svn <http://pylonshq.com/svn/WebHelpers/trunk#egg=WebHelpers-dev>`_

""",
    author='Ben Bangert, James Gardner',
    author_email='ben@groovie.org',
    url='http://pylonshq.com/WebHelpers/',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "Routes>=1.1",
        ],
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: BSD License",
                 "Programming Language :: Python",
                 "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
                 "Topic :: Software Development :: Libraries :: Python Modules",
               ],
    entry_points="""
    [paste.paster_command]
    scriptaculous=railshelpers.commands:ScriptaculousCommand
    """,
)
