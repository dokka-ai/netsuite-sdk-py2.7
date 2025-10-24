from __future__ import absolute_import
from .base import ApiBase
import logging
from datetime import datetime

from ..internal.utils import PaginatedSearch

logger = logging.getLogger(__name__)


class CurrencyRate(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'CurrencyRate')

    def get_by_date(self, search_date, base_currency, transaction_currency):
        # old deprecated version
        base_currency = self.ns_client.RecordRef(internalId=base_currency, type="currency")
        transaction_currency = self.ns_client.RecordRef(internalId=transaction_currency, type="currency")

        basic_search = self.ns_client.basic_search_factory(
            u'CurrencyRate',
            effectiveDate=self.ns_client.SearchDateField(searchValue=search_date, operator="onOrBefore"),
            baseCurrency=self.ns_client.SearchMultiSelectField(searchValue=base_currency, operator="anyOf"),
            transactionCurrency=self.ns_client.SearchMultiSelectField(searchValue=transaction_currency, operator="anyOf"),
        )

        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name=u'CurrencyRate',
                                           # search_record=self.ns_client.CurrencyRateSearchBasic(),
                                           basic_search=basic_search,
                                           pageSize=20)
        return list(self._paginated_search_to_generator(paginated_search=paginated_search))

    def get_by_dates(self, from_date: datetime, to_date: datetime, base_currency, transaction_currency):
        # new optimized version

        base_currency = self.ns_client.RecordRef(internalId=base_currency, type="currency")
        transaction_currency = self.ns_client.RecordRef(internalId=transaction_currency, type="currency")

        basic_search = self.ns_client.basic_search_factory(
            u'CurrencyRate',
            effectiveDate=self.ns_client.SearchDateField(
                operator="within",
                searchValue=from_date,
                searchValue2=to_date,
            ),
            baseCurrency=self.ns_client.SearchMultiSelectField(searchValue=base_currency, operator="anyOf"),
            transactionCurrency=self.ns_client.SearchMultiSelectField(searchValue=transaction_currency, operator="anyOf"),
        )

        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name=u'CurrencyRate',
                                           # search_record=self.ns_client.CurrencyRateSearchBasic(),
                                           basic_search=basic_search,
                                           pageSize=20)
        return list(self._paginated_search_to_generator(paginated_search=paginated_search))
