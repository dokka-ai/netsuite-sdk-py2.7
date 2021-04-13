from __future__ import absolute_import
from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Vendors(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'Vendor')

    def post(self, data):
        vendor = self.ns_client.Vendor()

        vendor['companyName'] = data['companyName']
        vendor['externalId'] = data['externalId']

        res = self.ns_client.upsert(vendor)
        return self._serialize(res)


class VendorSubsidiaryRelationships(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'VendorSubsidiaryRelationship')
