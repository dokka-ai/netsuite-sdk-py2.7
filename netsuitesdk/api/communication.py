from __future__ import absolute_import
import logging

from .base import ApiBase


logger = logging.getLogger(__name__)


class Note(ApiBase):

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name=u'Note')

    def post(self, data):
        """
        :param dict data:
            have to contain values:
                - transaction
                - title
                - note
        """
        txn_id = data.pop('transaction')
        transaction = self.ns_client.RecordRef(externalId=txn_id)
        note = self.ns_client.Note(
            transaction=transaction,
            **data
        )
        res = self.ns_client.add(note)
        return self._serialize(res)
