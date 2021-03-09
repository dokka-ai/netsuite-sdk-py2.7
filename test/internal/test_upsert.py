from __future__ import absolute_import
import logging
import pytest
import zeep
import datetime

from netsuitesdk.internal.utils import PaginatedSearch

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

def get_tax(ns):
    return get_record(ns, u'SalesTaxItem')

def get_vendor(ns):
    return get_record(ns, u'Vendor')

def get_category_account(ns):
    return ns.get(recordType=u'account', internalId=119)

def get_currency(ns):
    return ns.get(recordType=u'currency', internalId=u'1')

def get_employee(ns):
    return ns.get(recordType=u'employee', internalId=u'5')

def nottest_upsert_vendor_bill_expense(ns):
    vendor_ref = ns.RecordRef(type=u'vendor', internalId=7)
    category = ns.RecordRef(type=u'expenseCategory', internalId=1)
    cat_account_ref = ns.RecordRef(type=u'account', internalId=58)
    loc_ref = ns.RecordRef(type=u'location', internalId=get_location(ns).internalId)
    dep_ref = ns.RecordRef(type=u'department', internalId=get_department(ns).internalId)
    class_ref = ns.RecordRef(type=u'classification', internalId=get_department(ns).internalId)


    expenses = []

    vbe1 = ns.VendorBillExpense()
    vbe1[u'account'] = cat_account_ref
    vbe1[u'amount'] = 10.0
    vbe1[u'category'] = category
    vbe1[u'department'] = dep_ref
    vbe1[u'class'] = class_ref
    vbe1[u'location'] = loc_ref
    vbe1[u'memo'] = "expense 1"
    vbe1[u'taxCode'] = ns.RecordRef(type=u'salesTaxItem', internalId=6)

    expenses.append(vbe1)
    vbe1 = ns.VendorBillExpense()
    vbe1[u'account'] = cat_account_ref
    vbe1[u'amount'] = 20.0
    vbe1[u'category'] = category
    vbe1[u'department'] = dep_ref
    vbe1[u'class'] = class_ref
    vbe1[u'location'] = loc_ref
    vbe1[u'memo'] = "expense 2"
    vbe1[u'taxCode'] = ns.RecordRef(type=u'salesTaxItem', internalId=6)

    expenses.append(vbe1)
    externalId = u'1265'
    bill = ns.VendorBill(externalId=externalId)
    bill[u'currency'] = ns.RecordRef(type=u'currency', internalId=get_currency(ns).internalId) # US dollar
    bill[u'exchangerate'] = 1.0
    bill[u'approvalStatus'] = {'internalId': 1}
    bill[u'expenseList'] = ns.VendorBillExpenseList(expense=expenses)
    bill[u'memo'] = u'External Id' + externalId
    bill[u'postingPeriod'] = u'158'
    # bill[u'class'] = class_ref
    # bill[u'location'] = loc_ref
    bill[u'entity'] = vendor_ref
    logger.debug(u'upserting bill %s', bill)
    # print bill
    record_ref = ns.upsert(bill)
    logger.debug(u'record_ref = %s', record_ref)
    assert record_ref[u'externalId'] == externalId, u'External ID does not match'

    bill2 = ns.get(recordType=u'vendorBill', externalId=externalId)
    logger.debug(u'bill2 = %s', unicode(bill2))
    print bill2[u'userTotal']
    assert (29.99 < bill2[u'userTotal']) and (bill2[u'userTotal'] < 36), u'Bill total is not 30.0'


def test_upsert_vendor_bill_items(ns):
    external_id = u'123456'
    vendor_id = u'7'
    currency_id = u'1'
    posting_period_id = u'128'
    approval_status_id = u'1'

    bill = ns.VendorBill(externalId=external_id)

    bill[u'externalId'] = external_id
    bill[u'entity'] = ns.RecordRef(u'vendor', internalId=vendor_id)
    # Transaction Type
    bill[u'postingPeriod'] = posting_period_id
    bill[u'tranDate'] = datetime.date.today()
    bill[u'dueDate'] = datetime.date.today()
    bill[u'tranId'] = external_id
    bill[u'currency'] = ns.RecordRef(type=u'salesTaxItem', internalId=currency_id)
    bill[u'exchangerate'] = 1.1
    bill[u'approvalStatus'] = {'internalId': approval_status_id}
    bill[u'memo'] = "memo"


    expenses = []

    vbi = ns.VendorBillItem()
    vbi[u'item'] = ns.RecordRef(internalId=u'8')
    vbi[u'quantity'] = 1
    vbi[u'units'] = 'PSC'
    vbi[u'description'] = 'tabel description'
    vbi[u'rate'] = 1
    vbi[u'amount'] = vbi[u'quantity'] * vbi[u'rate']
    vbi[u'taxCode'] = ns.RecordRef(type=u'salesTaxItem', internalId=6)
    vbi[u'tax1Amt'] = vbi[u'amount'] * 0.17
    vbi[u'grossAmt'] = vbi[u'amount'] + vbi[u'tax1Amt']
    vbi[u'location'] = ns.RecordRef(type=u'location', internalId=1)
    vbi[u'class'] = ns.RecordRef(type=u'classification', internalId=1)
    vbi[u'department'] = ns.RecordRef(type=u'department', internalId=1)


    expenses.append(vbi)
    bill[u'itemList'] = ns.VendorBillItemList(item=expenses)
    # print bill
    record_ref = ns.upsert(bill)

    logger.debug(u'record_ref = %s', record_ref)
    # print record_ref[u'externalId']
    # exit(1)
    assert record_ref[u'externalId'] == external_id, u'External ID does not match'

    bill2 = ns.get(recordType=u'vendorBill', externalId=external_id)
    logger.debug(u'bill2 = %s', unicode(bill2))
    print bill2[u'userTotal']
    assert (0< bill2[u'userTotal']) and (bill2[u'userTotal'] < 2), u'Bill total is not 30.0'
# def test_upsert_journal_entry(ns):
#     vendor_ref = ns.RecordRef(type=u'vendor', internalId=get_vendor(ns).internalId)
#     cat_account_ref = ns.RecordRef(type=u'account', internalId=get_category_account(ns).internalId)
#     loc_ref = ns.RecordRef(type=u'location', internalId=get_location(ns).internalId)
#     dep_ref = ns.RecordRef(type=u'department', internalId=get_department(ns).internalId)
#     class_ref = ns.RecordRef(type=u'classification', internalId=get_department(ns).internalId)
#     lines = []
#
#     credit_line = ns.JournalEntryLine()
#     credit_line[u'account'] = cat_account_ref
#     credit_line[u'department'] = dep_ref
#     credit_line[u'class'] = class_ref
#     credit_line[u'location'] = loc_ref
#     credit_line[u'entity'] = vendor_ref
#     credit_line[u'credit'] = 20.0
#
#     lines.append(credit_line)
#
#     debit_line = ns.JournalEntryLine()
#     debit_line[u'account'] = cat_account_ref
#     debit_line[u'department'] = dep_ref
#     debit_line[u'class'] = class_ref
#     debit_line[u'location'] = loc_ref
#     debit_line[u'entity'] = vendor_ref
#     debit_line[u'debit'] = 20.0
#
#     lines.append(debit_line)
#
#     journal_entry = ns.JournalEntry(externalId=u'JE_1234')
#     journal_entry[u'currency'] = ns.RecordRef(type=u'currency', internalId=get_currency(ns).internalId)  # US dollar
#     journal_entry[u'subsidiary'] = ns.RecordRef(type=u'subsidiary', internalId=u'1')
#     journal_entry[u'exchangerate'] = 1.0
#     journal_entry[u'lineList'] = ns.JournalEntryLineList(line=lines)
#     journal_entry[u'memo'] = u'test memo'
#     logger.debug(u'upserting journal entry %s', journal_entry)
#     record_ref = ns.upsert(journal_entry)
#     logger.debug(u'record_ref = %s', record_ref)
#     assert record_ref[u'externalId'] == u'JE_1234', u'External ID does not match'
#
#     je = ns.get(recordType=u'journalEntry', externalId=u'JE_1234')
#     logger.debug(u'je = %s', unicode(je))
#     assert (je[u'externalId'] == u'JE_1234'), u'Journal Entry External ID does not match'
#
#
# def test_upsert_expense_report(ns):
#     employee_ref = ns.RecordRef(type=u'employee', internalId=get_employee(ns).internalId)
#     bill_account_ref = ns.RecordRef(type=u'account', internalId=25)
#     cat_account_ref = ns.RecordRef(type=u'account', internalId=u'1')
#     loc_ref = ns.RecordRef(type=u'location', internalId=get_location(ns).internalId)
#     dep_ref = ns.RecordRef(type=u'department', internalId=get_department(ns).internalId)
#     class_ref = ns.RecordRef(type=u'classification', internalId=get_department(ns).internalId)
#     currency_ref = ns.RecordRef(type=u'currency', internalId=get_currency(ns).internalId)
#     expenses = []
#
#     er = ns.ExpenseReportExpense()
#     er[u'category'] = cat_account_ref
#     er[u'amount'] = 10.0
#     er[u'department'] = dep_ref
#     er[u'class'] = class_ref
#     er[u'location'] = loc_ref
#     er[u'currency'] = currency_ref
#
#     expenses.append(er)
#
#     expense_report = ns.ExpenseReport(externalId=u'EXPR_1')
#     expense_report[u'expenseReportCurrency'] = currency_ref  # US dollar
#     expense_report[u'exchangerate'] = 1.0
#     expense_report[u'expenseList'] = ns.ExpenseReportExpenseList(expense=expenses)
#     expense_report[u'memo'] = u'test memo'
#     expense_report[u'entity'] = employee_ref
#     logger.debug(u'upserting expense report %s', expense_report)
#     record_ref = ns.upsert(expense_report)
#     logger.debug(u'record_ref = %s', record_ref)
#     assert record_ref[u'externalId'] == u'EXPR_1', u'External ID does not match'
#
#     expr = ns.get(recordType=u'ExpenseReport', externalId=u'EXPR_1')
#     logger.debug(u'expense report = %s', unicode(expr))
