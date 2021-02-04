import os
import itertools
import json
from netsuitesdk import NetSuiteConnection
from pprint import pprint
import time
start_time = time.time()
NS_ACCOUNT = "6758546"
NS_CONSUMER_KEY = "f0fbdf22d73942afd2433de153a84c19dcd408a4c2d54aac6ecf83f84ee763b0"
NS_CONSUMER_SECRET = "90369bc8c290ac61fb12b43e57f13fdbd0394b9f868622cf7924173755a15ac3"
NS_TOKEN_KEY = "fdf42bd9aeb7366b79d97654f0f0c30a3ab3192ae4d1180e2749ac59d8d188bf"
NS_TOKEN_SECRET = "339c8b3c2b0bef4b904ef30595e9dd2e234249f949e7baee35c372766fb1f354"
WSDL_URL = "https://webservices.netsuite.com/wsdl/v2020_1_0/netsuite.wsdl"

nc = NetSuiteConnection(
    account=NS_ACCOUNT,
    consumer_key=NS_CONSUMER_KEY,
    consumer_secret=NS_CONSUMER_SECRET,
    token_key=NS_TOKEN_KEY,
    token_secret=NS_TOKEN_SECRET
)
# result = nc.getDataCenterUrls()
# print(result)
# exit(1)
# print(nc)
# exit(1)
# Use get_all methods to get all objects of certain types

currencies = nc.currencies.get_all()

locations = nc.locations.get_all()
departments = nc.departments.get_all()
classifications = nc.classifications.get_all()
#subsidiaries = nc.subsidiaries.get_all()
expense_categories = nc.expense_categories.get_all()
employees = nc.employees.get_all()
all_accounts = list(itertools.islice(nc.accounts.get_all_generator(), 100))
accounts = [a for a in all_accounts if a['acctType'] == '_expense']
vendor_bills = list(itertools.islice(nc.vendor_bills.get_all_generator(), 10))
vendors = list(itertools.islice(nc.vendors.get_all_generator(), 10))
vendor_payments = nc.vendor_payments.get_all()

pprint(vendor_bills)
# data = {
#   'accounts': accounts,
#   'classifications': classifications,
#   'departments': departments,
#   'locations': locations,
#   #'currencies': currencies,
#   'vendors': vendors,
#   'vendor_bills': vendor_bills,
#   #'subsidiaries': subsidiaries,
#   'expense_categories': expense_categories,
#   'employees': employees,
#   'vendor_payments': vendor_payments
# }
# pprint(data)
#print("--- %s seconds ---" % (time.time() - start_time))
