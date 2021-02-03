from __future__ import absolute_import
from netsuitesdk.internal.utils import PaginatedSearch
import logging
import pytest
import zeep

logger = logging.getLogger(__name__)

#@pytest.mark.parametrize('type_name', ['Account', 'Vendor', 'Department', 'Location', 'Classification'])
def get_record(ns, type_name):
    paginated_search = PaginatedSearch(client=ns, type_name=type_name, pageSize=20)
    return paginated_search.records[0]

def get_location(ns):
    return get_record(ns, u'Location')

def get_department(ns):
    return get_record(ns, u'Department')

def get_class(ns):
    return get_record(ns, u'Classification')

def get_vendor(ns):
    return get_record(ns, u'Vendor')

def get_category_account(ns):
    return ns.get(recordType=u'account', internalId=84)

def get_currency(ns):
    return ns.get(recordType=u'currency', internalId=u'1')

def get_employee(ns):
    return ns.get(recordType=u'employee', internalId=u'1648')

def test_upsert_vendor_bill(ns):
    vendor_ref = ns.RecordRef(type=u'vendor', internalId=get_vendor(ns).internalId)
    bill_account_ref = ns.RecordRef(type=u'account', internalId=25)
    cat_account_ref = ns.RecordRef(type=u'account', internalId=get_category_account(ns).internalId)
    loc_ref = ns.RecordRef(type=u'location', internalId=get_location(ns).internalId)
    dep_ref = ns.RecordRef(type=u'department', internalId=get_department(ns).internalId)
    class_ref = ns.RecordRef(type=u'classification', internalId=get_department(ns).internalId)
    expenses = []

    vbe1 = ns.VendorBillExpense()
    vbe1[u'account'] = cat_account_ref
    vbe1[u'amount'] = 10.0
    vbe1[u'department'] = dep_ref
    vbe1[u'class'] = class_ref
    vbe1[u'location'] = loc_ref

    expenses.append(vbe1)
    vbe1 = ns.VendorBillExpense()
    vbe1[u'account'] = cat_account_ref
    vbe1[u'amount'] = 20.0
    vbe1[u'department'] = dep_ref
    vbe1[u'class'] = class_ref
    vbe1[u'location'] = loc_ref

    expenses.append(vbe1)

    bill = ns.VendorBill(externalId=u'1234')
    bill[u'currency'] = ns.RecordRef(type=u'currency', internalId=get_currency(ns).internalId) # US dollar
    bill[u'exchangerate'] = 1.0
    bill[u'expenseList'] = ns.VendorBillExpenseList(expense=expenses)
    bill[u'memo'] = u'test memo'
    bill[u'class'] = class_ref
    bill[u'location'] = loc_ref
    bill[u'entity'] = vendor_ref
    logger.debug(u'upserting bill %s', bill)
    record_ref = ns.upsert(bill)
    logger.debug(u'record_ref = %s', record_ref)
    assert record_ref[u'externalId'] == u'1234', u'External ID does not match'

    bill2 = ns.get(recordType=u'vendorBill', externalId=u'1234')
    logger.debug(u'bill2 = %s', unicode(bill2))
    assert (29.99 < bill2[u'userTotal']) and (bill2[u'userTotal'] < 30.01), u'Bill total is not 30.0'

def test_upsert_journal_entry(ns):
    vendor_ref = ns.RecordRef(type=u'vendor', internalId=get_vendor(ns).internalId)
    cat_account_ref = ns.RecordRef(type=u'account', internalId=get_category_account(ns).internalId)
    loc_ref = ns.RecordRef(type=u'location', internalId=get_location(ns).internalId)
    dep_ref = ns.RecordRef(type=u'department', internalId=get_department(ns).internalId)
    class_ref = ns.RecordRef(type=u'classification', internalId=get_department(ns).internalId)
    lines = []

    credit_line = ns.JournalEntryLine()
    credit_line[u'account'] = cat_account_ref
    credit_line[u'department'] = dep_ref
    credit_line[u'class'] = class_ref
    credit_line[u'location'] = loc_ref
    credit_line[u'entity'] = vendor_ref
    credit_line[u'credit'] = 20.0

    lines.append(credit_line)

    debit_line = ns.JournalEntryLine()
    debit_line[u'account'] = cat_account_ref
    debit_line[u'department'] = dep_ref
    debit_line[u'class'] = class_ref
    debit_line[u'location'] = loc_ref
    debit_line[u'entity'] = vendor_ref
    debit_line[u'debit'] = 20.0

    lines.append(debit_line)

    journal_entry = ns.JournalEntry(externalId=u'JE_1234')
    journal_entry[u'currency'] = ns.RecordRef(type=u'currency', internalId=get_currency(ns).internalId)  # US dollar
    journal_entry[u'subsidiary'] = ns.RecordRef(type=u'subsidiary', internalId=u'1')
    journal_entry[u'exchangerate'] = 1.0
    journal_entry[u'lineList'] = ns.JournalEntryLineList(line=lines)
    journal_entry[u'memo'] = u'test memo'
    logger.debug(u'upserting journal entry %s', journal_entry)
    record_ref = ns.upsert(journal_entry)
    logger.debug(u'record_ref = %s', record_ref)
    assert record_ref[u'externalId'] == u'JE_1234', u'External ID does not match'

    je = ns.get(recordType=u'journalEntry', externalId=u'JE_1234')
    logger.debug(u'je = %s', unicode(je))
    assert (je[u'externalId'] == u'JE_1234'), u'Journal Entry External ID does not match'


def test_upsert_expense_report(ns):
    employee_ref = ns.RecordRef(type=u'employee', internalId=get_employee(ns).internalId)
    bill_account_ref = ns.RecordRef(type=u'account', internalId=25)
    cat_account_ref = ns.RecordRef(type=u'account', internalId=u'1')
    loc_ref = ns.RecordRef(type=u'location', internalId=get_location(ns).internalId)
    dep_ref = ns.RecordRef(type=u'department', internalId=get_department(ns).internalId)
    class_ref = ns.RecordRef(type=u'classification', internalId=get_department(ns).internalId)
    currency_ref = ns.RecordRef(type=u'currency', internalId=get_currency(ns).internalId)
    expenses = []

    er = ns.ExpenseReportExpense()
    er[u'category'] = cat_account_ref
    er[u'amount'] = 10.0
    er[u'department'] = dep_ref
    er[u'class'] = class_ref
    er[u'location'] = loc_ref
    er[u'currency'] = currency_ref

    expenses.append(er)

    expense_report = ns.ExpenseReport(externalId=u'EXPR_1')
    expense_report[u'expenseReportCurrency'] = currency_ref  # US dollar
    expense_report[u'exchangerate'] = 1.0
    expense_report[u'expenseList'] = ns.ExpenseReportExpenseList(expense=expenses)
    expense_report[u'memo'] = u'test memo'
    expense_report[u'entity'] = employee_ref
    logger.debug(u'upserting expense report %s', expense_report)
    record_ref = ns.upsert(expense_report)
    logger.debug(u'record_ref = %s', record_ref)
    assert record_ref[u'externalId'] == u'EXPR_1', u'External ID does not match'

    expr = ns.get(recordType=u'ExpenseReport', externalId=u'EXPR_1')
    logger.debug(u'expense report = %s', unicode(expr))
