from netsuitesdk.connection import NetSuiteConnection
import os
import datetime

from netsuitesdk.internal.client import NetSuiteClient

NS_ACCOUNT = os.getenv(u'NS_ACCOUNT')
NS_CONSUMER_KEY = os.getenv(u'NS_CONSUMER_KEY')
NS_CONSUMER_SECRET = os.getenv(u'NS_CONSUMER_SECRET')
NS_TOKEN_KEY = os.getenv(u'NS_TOKEN_KEY')
NS_TOKEN_SECRET = os.getenv(u'NS_TOKEN_SECRET')

ns = NetSuiteConnection(account=NS_ACCOUNT,
                        consumer_key=NS_CONSUMER_KEY,
                        consumer_secret=NS_CONSUMER_SECRET,
                        token_key=NS_TOKEN_KEY,
                        token_secret=NS_TOKEN_SECRET)

items = ns.items.get_all()

print items

exit(1)

external_id = u'123467'
vendor_id = u'7'
currency_id = u'1'
posting_period_id = u'107'
approval_status_id = u'1'

bill = ns.VendorBill(externalId=external_id)

# bill[u'externalId'] = external_id
bill[u'entity'] = ns.RecordRef(u'vendor', internalId=vendor_id)
# Transaction Type
# bill[u'postingPeriod'] = posting_period_id
# bill[u'tranDate'] = datetime.datetime(2021, 04, 5, 18, 00)
# bill[u'dueDate'] = datetime.datetime(2021, 04, 25, 18, 00)
# bill[u'tranId'] = external_id
# bill[u'currency'] = ns.RecordRef(type=u'salesTaxItem', internalId=currency_id)
# bill[u'exchangerate'] = 1.1
# bill[u'approvalStatus'] = {'internalId': approval_status_id}
# bill[u'memo'] = "memo"


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

purchaseOrder = ns.RecordRef(type='purchaseOrder', internalId=112, name="MyName")

bill.purchaseOrderList = ns.RecordRefList([purchaseOrder])

# internalId
# externalId
# type
# name

expenses.append(vbi)

purchaseOrderList = [purchaseOrder]
bill.purchaseOrderList = purchaseOrderList

# bill['purchaseOrderList'] =ns.RecordRefList(type="purchaseOrderList", purchaseOrder=purchaseOrderList)
# print bill
record_ref = ns.add(bill)

print record_ref
