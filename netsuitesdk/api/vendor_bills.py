from __future__ import absolute_import
import logging

from ..internal.utils import PaginatedSearch

from .base import ApiBase
from typing import List
from collections import OrderedDict

logger = logging.getLogger(__name__)


class VendorBills(ApiBase):
    u"""
    VendorBills are not directly searchable - only via as transactions
    """

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'vendorBill')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue=u'VendorBill', operator=u'contains')
        basic_search = self.ns_client.basic_search_factory(u'Transaction', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name=u'Transaction',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def get_vendor_and_txn_id(self, vendor_id, txn_id):
        record_type_search_field = self.ns_client.SearchStringField(searchValue=u'VendorBill', operator=u'contains')
        tranx_id_search_field = self.ns_client.SearchStringField(searchValue=txn_id, operator=u'contains')
        entity = self.ns_client.RecordRef(internalId=vendor_id, type="vendorBill")
        vendor_id_search_field = self.ns_client.SearchMultiSelectField(searchValue=entity, operator=u'anyOf')
        basic_search = self.ns_client.basic_search_factory(
            u'Transaction',
            recordType=record_type_search_field,
            entity=vendor_id_search_field,
            tranId=tranx_id_search_field
        )
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name=u'Transaction',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data):
        assert data[u'externalId'], u'missing external id'
        vb = self.ns_client.VendorBill(externalId=data[u'externalId'])
        expense_list = []
        for eod in data[u'expenseList']:
            if u'customFieldList' in eod and eod[u'customFieldList']:
                custom_fields = []
                for field in eod[u'customFieldList']:
                    if field[u'type'] == u'String':
                        custom_fields.append(
                            self.ns_client.StringCustomFieldRef(
                                scriptId=field[u'scriptId'] if u'scriptId' in field else None,
                                internalId=field[u'internalId'] if u'internalId' in field else None,
                                value=field[u'value']
                            )
                        )
                    elif field[u'type'] == u'Select':
                        custom_fields.append(
                            self.ns_client.SelectCustomFieldRef(
                                scriptId=field[u'scriptId'] if u'scriptId' in field else None,
                                internalId=field[u'internalId'] if u'internalId' in field else None,
                                value=self.ns_client.ListOrRecordRef(
                                    internalId=field[u'value']
                                )
                            )
                        )
                eod[u'customFieldList'] = self.ns_client.CustomFieldList(custom_fields)
            vbe = self.ns_client.VendorBillExpense(**eod)
            expense_list.append(vbe)

        vb[u'expenseList'] = self.ns_client.VendorBillExpenseList(expense=expense_list)
        vb[u'currency'] = self.ns_client.RecordRef(**(data[u'currency']))

        if u'memo' in data:
            vb[u'memo'] = data[u'memo']

        if u'tranDate' in data:
            vb[u'tranDate'] = data[u'tranDate']

        if u'tranId' in data:
            vb[u'tranId'] = data[u'tranId']

        if u'class' in data:
            vb[u'class'] = self.ns_client.RecordRef(**(data[u'class']))

        if u'location' in data:
            vb[u'location'] = self.ns_client.RecordRef(**(data[u'location']))

        if u'department' in data:
            vb[u'department'] = self.ns_client.RecordRef(**(data[u'department']))

        if u'account' in data:
            vb[u'account'] = self.ns_client.RecordRef(**(data[u'account']))

        vb[u'entity'] = self.ns_client.RecordRef(**(data[u'entity']))
        logger.debug(u'able to create vb = %s', vb)
        res = self.ns_client.upsert(vb)
        return self._serialize(res)
