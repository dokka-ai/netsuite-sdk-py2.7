from __future__ import absolute_import
from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class AccountingPeriod(ApiBase):

	def __init__(self, ns_client):
		ApiBase.__init__(self, ns_client=ns_client, type_name=u'AccountingPeriod')

	@staticmethod
	def compare(item1, item2):
		q1, y1 = item1[0].split(" ")
		q2, y2 = item2[0].split(" ")

		if y1 > y2:
			return -1
		elif y1 < y2:
			return 1

		if y1 == y2:
			if q1 > q2:
				return -1
			else:
				return 1

	def get_periods(self):
		_p = {}
		for period in self.get_all():
			if not period['isQuarter'] and not period['isYear']:
				if period['parent']['name'] not in _p:
					_p.setdefault(period['parent']['name'], [])
				_p[period['parent']['name']].append((period['internalId'], period['periodName']))

		dictionary_items = _p.items()
		sorted_items = sorted(dictionary_items, cmp=self.compare)

		periods = []
		for q in sorted_items:
			periods.append({'internalId': 0, 'name': q[0]})
			for i in reversed(q[1]):
				periods.append({'internalId': i[0], 'name': ' ' + i[1]})

		return periods
