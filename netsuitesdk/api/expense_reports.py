from __future__ import absolute_import
from collections import OrderedDict

from .base import ApiBase
import logging

from netsuitesdk.internal.utils import PaginatedSearch

logger = logging.getLogger(__name__)


class ExpenseReports(ApiBase):
    u"""
    ExpenseReports are not directly searchable - only via as employees
    """

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'ExpenseReport')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue=u'ExpenseReport', operator=u'contains')
        basic_search = self.ns_client.basic_search_factory(u'Employee', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name=u'Employee',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data):
        assert data[u'externalId'], u'missing external id'
        er = self.ns_client.ExpenseReport()
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
            ere = self.ns_client.ExpenseReportExpense(**eod)
            expense_list.append(ere)

        er[u'expenseList'] = self.ns_client.ExpenseReportExpenseList(expense=expense_list)
        er[u'expenseReportCurrency'] = self.ns_client.RecordRef(**(data[u'expenseReportCurrency']))

        if u'memo' in data:
            er[u'memo'] = data[u'memo']

        if u'tranDate' in data:
            er[u'tranDate'] = data[u'tranDate']

        if u'tranId' in data:
            er[u'tranId'] = data[u'tranId']

        if u'class' in data:
            er[u'class'] = data[u'class']

        if u'location' in data:
            er[u'location'] = data[u'location']

        if u'department' in data:
            er[u'department'] = data[u'department']

        if u'account' in data:
            er[u'account'] = self.ns_client.RecordRef(**(data[u'account']))

        if u'accountingApproval' in data:
            er[u'accountingApproval'] = data[u'accountingApproval']

        if u'supervisorApproval' in data:
            er[u'supervisorApproval'] = data[u'supervisorApproval']

        if u'externalId' in data:
            er[u'externalId'] = data[u'externalId']

        er[u'entity'] = self.ns_client.RecordRef(**(data[u'entity']))
        logger.debug(u'able to create er = %s', er)
        res = self.ns_client.upsert(er)
        return self._serialize(res)
