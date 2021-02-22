from __future__ import absolute_import
from ..internal.utils import PaginatedSearch

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class CustomRecords(ApiBase):
    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'CustomRecordType')

    def get_all_by_id(self, internalId):
        cr_type = self.ns_client.CustomRecordSearchBasic(
            recType=self.ns_client.CustomRecordType(
                internalId=internalId
            )
        )
        ps = PaginatedSearch(client=self.ns_client, type_name=u'CustomRecordType', search_record=cr_type, pageSize=20)
        return list(self._paginated_search_to_generator(paginated_search=ps))
