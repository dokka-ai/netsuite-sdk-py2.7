from __future__ import absolute_import
from .base import ApiBase
import logging

from ..internal.utils import PaginatedSearch

logger = logging.getLogger(__name__)


class CurrencyRate(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'CurrencyRate')

    def get_by_date(self, search_date, base_currency, transaction_currency):
        base_currency = self.ns_client.RecordRef(internalId=base_currency, type="currency")
        transaction_currency = self.ns_client.RecordRef(internalId=transaction_currency, type="currency")

        basic_search = self.ns_client.row_basic_search_factory(
            u'CurrencyRate',
            effectiveDate=self.ns_client.SearchColumnDateField(searchValue=search_date),
            baseCurrency=self.ns_client.SearchColumnSelectField(searchValue=base_currency),
            transactionCurrency=self.ns_client.SearchColumnSelectField(searchValue=transaction_currency),
        )

        paginated_search = PaginatedSearch(client=self.ns_client,
                                           type_name=u'CurrencyRate',
                                           search_record=self.ns_client.CurrencyRateSearchBasic(),
                                           basic_search=basic_search,
                                           pageSize=20)
        return list(self._paginated_search_to_generator(paginated_search=paginated_search))
