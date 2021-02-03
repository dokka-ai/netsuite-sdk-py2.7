from __future__ import absolute_import
from netsuitesdk.internal.utils import PaginatedSearch
import logging
import pytest

logger = logging.getLogger(__name__)

def test_get_currency(ns):
    record = ns.get(recordType=u'currency', internalId=u'1')
    assert record, u'No currency record for internalId 1'

def test_get_vendor_bill(ns):
    record = ns.get(recordType=u'vendorBill', externalId=u'1234')
    assert record, u'No vendor bill found'


def test_get_journal_entry(ns):
    record = ns.get(recordType=u'journalEntry', externalId=u'JE_01')
    assert record, u'No journal entry found'

def test_get_employee(ns):
    record = ns.get(recordType=u'employee', internalId=u'1648')
    assert record, u'No employee record for internalId 1'

def test_get_expense_report(ns):
    record = ns.get(recordType=u'ExpenseReport', externalId=u'EXPR_1')
    assert record, u'No expense report found'

# def test_get_currency1(nc):
#     currency = nc.currency.get(internal_id='1')
#     logger.info('currency is %s', currency)
