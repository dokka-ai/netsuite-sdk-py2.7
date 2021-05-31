from __future__ import absolute_import
from .base import ApiBase
import logging

from ..internal.utils import PaginatedSearch

logger = logging.getLogger(__name__)


class AmortizationTemplate(ApiBase):

	def __init__(self, ns_client):
		ApiBase.__init__(self, ns_client=ns_client, type_name=u'RevRecTemplate')

	# def get_all(self, page_size=50):
	# 	self.ns_client.set_search_preferences(return_search_columns=True)
	# 	_false = self.ns_client.SearchBooleanField(searchValue=False)
	# 	basic_search = self.ns_client.basic_search_factory(
	# 		u'RevRecTemplate',
	# 		# isInactive=_false,
	# 	)
	# 	paginated_search = PaginatedSearch(client=self.ns_client,
	# 	                                   type_name='RevRecTemplate',
	# 	                                   basic_search=basic_search,
	# 	                                   pageSize=page_size)
	#
	# 	return list(self._paginated_search_to_generator(paginated_search=paginated_search))
