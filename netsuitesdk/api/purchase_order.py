from __future__ import absolute_import
from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class PurchaseOrder(ApiBase):

    def post(self, data):
        pass

    def __init__(self, ns_client):
        api = ApiBase.__init__(self, ns_client=ns_client, type_name=u'Transaction')

    def get(self):
        orders = []
        orders_raw = self.get_all()

        for order in orders_raw:
            if 'transactionNumber' not in order and 'availableVendorCredit' in order:
                orders.append(order)
        return orders

