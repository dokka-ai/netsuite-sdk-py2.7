from __future__ import with_statement
from __future__ import absolute_import
import setuptools
from io import open

with open(u'README.md', u'r') as f:
    long_description = f.read()

setuptools.setup(
    name=u'netsuitesdk',
    version=u'1.14.11',
    author=u'Siva Narayanan',
    author_email=u'siva@fyle.in',
    description=u'Python SDK for accessing the NetSuite SOAP webservice',
    license=u'MIT',
    long_description=long_description,
    long_description_content_type=u'text/markdown',
    keywords=[u'netsuite', u'api', u'python', u'sdk'],
    url=u'https://github.com/fylein/netsuite-sdk-py',
    packages=setuptools.find_packages(),
    install_requires=[u'zeep'],
    classifiers=[
        u'Topic :: Internet :: WWW/HTTP',
        u'Intended Audience :: Developers',
        u'Programming Language :: Python :: 3',
        u'License :: OSI Approved :: MIT License',
        u'Operating System :: OS Independent',
    ]
)
