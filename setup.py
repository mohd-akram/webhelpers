try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

version = '1.0b1'

setup(
    name="WebHelpers",
    version=version,
    description='Web Helpers',
    long_description="""
Web Helpers is a library of helper functions intended to make writing 
templates in web applications easier. It's the standard function library for
Pylons and TurboGears 2.  It also contains a large number of functions not
specific to the web, including text processing, number formatting, date
calculations, container objects, etc.

Complete documentation is in the docstrings in the source code.  Questions or
feedback about WebHelpers can be submitted to the `pylons-discuss
<http://groups.google.com/group/pylons-discuss>`_ mailing list. 

A few of these helpers require `Routes <http://routes.groovie.org/>`_ 
to function.

* `Development version <http://bitbucket.org/bbangert/webhelpers>`_
  (Mercurial)

""",
    author='Mike Orr, Ben Bangert, Phil Jenvey',
    author_email='sluggoster@gmail.com, ben@groovie.org, pjenvey@groovie.org',
    url='http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        ],
    tests_require=[ 
      'nose',
      'routes'
      ], 
    test_suite='nose.collector',
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
