from __future__ import absolute_import
from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class Currencies(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'Currency')

    def get_all(self):
        return self._get_all()

    def get_all_generator(self, page_size=20):
        u"""
        Returns a generator which is more efficient memory-wise
        """
        return self._get_all_generator()
