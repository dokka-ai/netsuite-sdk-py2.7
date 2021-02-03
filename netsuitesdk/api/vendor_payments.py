from __future__ import absolute_import
import logging

from netsuitesdk.internal.utils import PaginatedSearch

from .base import ApiBase
from collections import OrderedDict

logger = logging.getLogger(__name__)


class VendorPayments(ApiBase):
    u"""
    VendorPayments are not directly searchable - only via as transactions
    """

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'vendorPayment')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue=u'VendorPayment', operator=u'contains')
        basic_search = self.ns_client.basic_search_factory(u'Transaction', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name=u'Transaction',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data):
        assert data[u'externalId'], u'missing external id'
        vp = self.ns_client.VendorPayment(externalId=data[u'externalId'])
        apply_lists = []
        for eod in data[u'applyList'][u'apply']:
            vpal = self.ns_client.VendorPaymentApply(**eod)
            apply_lists.append(vpal)

        vp[u'applyList'] = self.ns_client.VendorPaymentApplyList(apply=apply_lists)
        vp[u'currency'] = self.ns_client.RecordRef(**(data[u'currency']))

        if u'amount' in data:
            vp[u'amount'] = data[u'amount']

        if u'memo' in data:
            vp[u'memo'] = data[u'memo']

        if u'tranDate' in data:
            vp[u'tranDate'] = data[u'tranDate']

        if u'tranId' in data:
            vp[u'tranId'] = data[u'tranId']

        if u'class' in data:
            vp[u'class'] = self.ns_client.RecordRef(**(data[u'class']))

        if u'location' in data:
            vp[u'location'] = self.ns_client.RecordRef(**(data[u'location']))

        if u'department' in data:
            vp[u'department'] = self.ns_client.RecordRef(**(data[u'department']))

        if u'account' in data:
            vp[u'account'] = self.ns_client.RecordRef(**(data[u'account']))

        if u'externalId' in data:
            vp[u'externalId'] = data[u'externalId']

        vp[u'entity'] = self.ns_client.RecordRef(**(data[u'entity']))
        logger.debug(u'able to create vp = %s', vp)
        res = self.ns_client.upsert(vp)
        return self._serialize(res)
