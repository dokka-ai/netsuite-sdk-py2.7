from __future__ import absolute_import
from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Files(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'File')

    def post(self, data):
        assert data[u'externalId'], u'missing external id'
        file = self.ns_client.File()

        if u'name' in data:
            file[u'name'] = data[u'name']

        if u'folder' in data:
            file[u'folder'] = self.ns_client.RecordRef(**(data[u'folder']))

        if u'externalId' in data:
            file[u'externalId'] = data[u'externalId']

        if u'content' in data:
            file[u'content'] = data[u'content']

        if u'mediaType' in data:
            file[u'mediaType'] = data[u'mediaType']

        logger.debug(u'able to create file = %s', file)
        res = self.ns_client.upsert(file)
        return self._serialize(res)
