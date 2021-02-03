from __future__ import absolute_import
from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Folders(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'Folder')

    def post(self, data):
        assert data[u'externalId'], u'missing external id'
        folder = self.ns_client.Folder()

        if u'name' in data:
            folder[u'name'] = data[u'name']

        if u'externalId' in data:
            folder[u'externalId'] = data[u'externalId']

        logger.debug(u'able to create folder = %s', folder)
        res = self.ns_client.upsert(folder)
        return self._serialize(res)
