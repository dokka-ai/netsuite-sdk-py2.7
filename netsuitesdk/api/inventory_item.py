from __future__ import absolute_import
from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class InventoryItem(ApiBase):

    def post(self, data):
        pass

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'Item')

