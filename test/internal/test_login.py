from __future__ import with_statement
from __future__ import absolute_import
import logging
import os
import time

import pytest
from netsuitesdk.internal.client import NetSuiteClient
from netsuitesdk.internal.utils import PaginatedSearch
from netsuitesdk.internal.exceptions import NetSuiteLoginError

logger = logging.getLogger(__name__)

def test_login_disallowed():
    u"""
    Test if login method is supported. We will not use this often.
    """
    NS_EMAIL = os.getenv(u"NS_EMAIL")
    NS_PASSWORD = os.getenv(u"NS_PASSWORD")
    NS_ROLE = os.getenv(u"NS_ROLE")
    NS_ACCOUNT = os.getenv(u"NS_ACCOUNT")
    NS_APPID = os.getenv(u"NS_APPID")
    ns = NetSuiteClient(account=NS_ACCOUNT)
    with pytest.raises(NetSuiteLoginError) as ex:
        ns.login(email=NS_EMAIL, password=NS_PASSWORD, role=NS_ROLE, application_id=NS_APPID)
    assert u'Integration blocked' in unicode(ex.value), u'credentials are allowing login - this is not recommended'
