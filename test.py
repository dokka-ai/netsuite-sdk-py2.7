from netsuitesdk.connection import NetSuiteConnection
import os
import datetime
from time import time
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


# start = time()

a = ns.vendor_bills.get_bill_by_transaction_number('VENDBILL440', 'vendorBill')
print len(a)
exit(0)


# bills = ns.vendor_bills.get_bill_by_txn_id(13892)
# for bill in bills:
#     for fields in bill:
#         print fields
# start = time()
# a = list(ns.vendor_bills.get_all_generator())
# print a
# print time() - start


# ns_client = NetSuiteClient(account=NS_ACCOUNT)
# ns_client.connect_tba(
#     consumer_key=NS_CONSUMER_KEY,
#     consumer_secret=NS_CONSUMER_SECRET,
#     token_key=NS_TOKEN_KEY,
#     token_secret=NS_TOKEN_SECRET
# )

# for i in range(0, 45):
#     try:
#         verbose_type_name = "ns{}:DateCustomFieldRef".format(i)
#         result = ns_client._client.get_type(verbose_type_name)
#         print verbose_type_name, result
#     except Exception as e:
#         pass
# r = ns_client.call_get_restlet("https://6758546.restlets.api.netsuite.com/app/site/hosting/restlet.nl?script=9&deploy=1",'getCustomFields',
#                                'vendorbill', "item,expense")
# print r
# exit(1)
# item_fields = (
# 			'internalId', 'expenseAccount', 'incomeAccount',
# 			'class', 'location', 'itemId', 'department', 'displayName',
# 			'vendorName', 'cost', 'unitsType', 'purchaseDescription',
# 			'otherVendor', 'vendorCost', 'vendorPriceCurrency', 'lastPurchasePrice'
# 		)
# items = ns.folders.get_all()
# for item in items:
#     print item

# exit(1)

# b = ns.items.get_all()
# for i in b:
#     print i
# print b
# exit(1)
# ns = NetSuiteClient(account=NS_ACCOUNT)
# ns.connect_tba(consumer_key=NS_CONSUMER_KEY,
#                consumer_secret=NS_CONSUMER_SECRET,
#                token_key=NS_TOKEN_KEY,
#                token_secret=NS_TOKEN_SECRET,
#                signature_algorithm=u'HMAC-SHA1')

subsidiaries = ns.currencyRate.get_all()
for s in subsidiaries:
    for i in s:
        print i, s[i]
    print "-----------------------------"
    # exit(1)

# pdf file
data = open('google1.pdf', 'r').read()

file = ns.File(name="google1.pdf", fileType="_PDF", content=data, folder=ns.RecordRef(type="folder", internalId="-12"))
a = ns.add(file)
attach_file = ns.AttachBasicReference()
attach_file.attachTo = ns.RecordRef()
attach_file.attachTo.internalId = 4029
attach_file.attachTo.type = "vendorBill"
attach_file.attachedRecord = ns.RecordRef()
attach_file.attachedRecord.internalId = a.internalId
attach_file.attachedRecord.type = "file"
p = ns.attach(attach_file)
print p
print a
exit(1)
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

purchaseOrder = ns.RecordRef(type='purchaseOrder', internalId=3326, name="MyName")

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
# record_ref = ns.add(bill)
#
# print record_ref

purchaseOrder2 = ns.InitializeRef(type='purchaseOrder', internalId=3326)

record = ns.InitializeRecord()
record.type = 'vendorBill'
record.referenceList = ns.InitializeRefList([purchaseOrder2])

record = ns.initialize(record)
print record
del record['exchangeRate']

fields = [u'item', u'quantity', u'units', u'description', u'rate', u'amount', u'taxCode', u'orderDoc', u'orderLine'
         u'tax1Amt', u'grossAmt', u'department', u'class', u'location', u'internalId', u'externalId']

new_items = []
for item in record['itemList']['item']:
    new_item = {}
    for field in item:
        # if field in fields:
        if field == "quantity":
            new_item.setdefault(field, 10)
        elif field != 'taxRate1':
            new_item.setdefault(field, item[field])
    new_items.append(new_item)

# record['purchaseOrderList'] = ns.RecordRefList([purchaseOrder])
record['itemList']['item'] = new_items
record['externalId'] = "138500"
r2 = ns.upsert(record)
print r2
