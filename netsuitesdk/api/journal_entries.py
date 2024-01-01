from __future__ import absolute_import
from collections import OrderedDict
from ..internal.utils import PaginatedSearch

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class JournalEntries(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'journalEntry')

    def get_all_generator(self):
        record_type_search_field = self.ns_client.SearchStringField(searchValue=u'JournalEntry', operator=u'contains')
        basic_search = self.ns_client.basic_search_factory(u'Transaction', recordType=record_type_search_field)
        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name=u'Transaction',
                                           basic_search=basic_search,
                                           pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def post(self, data):
        assert data[u'externalId'], u'missing external id'
        je = self.ns_client.JournalEntry(externalId=data[u'externalId'])
        line_list = []
        for eod in data[u'lineList']:
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
            jee = self.ns_client.JournalEntryLine(**eod)
            line_list.append(jee)

        je[u'lineList'] = self.ns_client.JournalEntryLineList(line=line_list)
        je[u'currency'] = self.ns_client.RecordRef(**(data[u'currency']))

        if u'exchangeRate' in data:
            je[u'exchangeRate'] = data[u'exchangeRate']

        if u'memo' in data:
            je[u'memo'] = data[u'memo']

        if u'tranDate' in data:
            je[u'tranDate'] = data[u'tranDate']

        if u'tranId' in data:
            je[u'tranId'] = data[u'tranId']

        if u'subsidiary' in data:
            je[u'subsidiary'] = data[u'subsidiary']

        if u'class' in data:
            je[u'class'] = data[u'class']

        if u'location' in data:
            je[u'location'] = data[u'location']

        if u'department' in data:
            je[u'department'] = data[u'department']

        logger.debug(u'able to create je = %s', je)
        res = self.ns_client.upsert(je)
        return self._serialize(res)
