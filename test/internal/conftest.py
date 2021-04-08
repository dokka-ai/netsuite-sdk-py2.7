from __future__ import absolute_import
import logging
import os

import pytest

from netsuitesdk.connection import NetSuiteConnection
from netsuitesdk.internal.client import NetSuiteClient

logger = logging.getLogger(__name__)

@pytest.fixture(scope=u'module')
def ns():
    u"""
    Returns: (ns, headers)
    """
    NS_ACCOUNT = os.getenv(u'NS_ACCOUNT')
    NS_CONSUMER_KEY = os.getenv(u'NS_CONSUMER_KEY')
    NS_CONSUMER_SECRET = os.getenv(u'NS_CONSUMER_SECRET')
    NS_TOKEN_KEY = os.getenv(u'NS_TOKEN_KEY')
    NS_TOKEN_SECRET = os.getenv(u'NS_TOKEN_SECRET')
    ns = NetSuiteClient(account=NS_ACCOUNT)
    ns.connect_tba(consumer_key=NS_CONSUMER_KEY,
                   consumer_secret=NS_CONSUMER_SECRET,
                   token_key=NS_TOKEN_KEY,
                   token_secret=NS_TOKEN_SECRET,
                   signature_algorithm=u'HMAC-SHA1')
    return ns


@pytest.fixture(scope=u'module')
def ns_connection():
    NS_ACCOUNT = os.getenv(u'NS_ACCOUNT')
    NS_CONSUMER_KEY = os.getenv(u'NS_CONSUMER_KEY')
    NS_CONSUMER_SECRET = os.getenv(u'NS_CONSUMER_SECRET')
    NS_TOKEN_KEY = os.getenv(u'NS_TOKEN_KEY')
    NS_TOKEN_SECRET = os.getenv(u'NS_TOKEN_SECRET')
    ns_connection = NetSuiteConnection(account=NS_ACCOUNT,
                                       consumer_key=NS_CONSUMER_KEY,
                                       consumer_secret=NS_CONSUMER_SECRET,
                                       token_key=NS_TOKEN_KEY,
                                       token_secret=NS_TOKEN_SECRET)
    return ns_connection
