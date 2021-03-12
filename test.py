from netsuitesdk.connection import NetSuiteConnection
import os

NS_ACCOUNT = os.getenv(u'NS_ACCOUNT')
NS_CONSUMER_KEY = os.getenv(u'NS_CONSUMER_KEY')
NS_CONSUMER_SECRET = os.getenv(u'NS_CONSUMER_SECRET')
NS_TOKEN_KEY = os.getenv(u'NS_TOKEN_KEY')
NS_TOKEN_SECRET = os.getenv(u'NS_TOKEN_SECRET')

ns = NetSuiteConnection(NS_ACCOUNT, NS_CONSUMER_KEY, NS_CONSUMER_SECRET, NS_TOKEN_KEY, NS_TOKEN_SECRET)

periods = ns.accountingPeriod.get_periods()

for p in periods:
    print p
