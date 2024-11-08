from __future__ import absolute_import
from .api.accounts import Accounts
from .api.classifications import Classifications, CostCategory
from .api.departments import Departments
from .api.currencies import Currencies
from .api.locations import Locations
from .api.vendor_bills import VendorBills
from .api.vendors import Vendors, VendorSubsidiaryRelationships
from .api.subsidiaries import Subsidiaries
from .api.journal_entries import JournalEntries
from .api.employees import Employees
from .api.expense_reports import ExpenseReports
from .api.folders import Folders
from .api.files import Files
from .api.customers import Customers
from .api.projects import Projects
from .api.expense_categories import ExpenseCategory
from .api.custom_lists import CustomLists
from .api.custom_records import CustomRecords
from .api.vendor_payments import VendorPayments
from .api.accountingPeriod import AccountingPeriod
from .api.taxtype import TaxType, TaxGroup
from .api.inventory_item import InventoryItem
from .api.unitstype import UnitsType
from .api.transactions import Transactions
from .api.terms import Terms
from .api.communication import Note
from .api.currencyRate import CurrencyRate
from .internal.client import NetSuiteClient
from .internal.utils import PaginatedSearch


class NetSuiteConnection(object):
    def __init__(self, account, consumer_key, consumer_secret, token_key, token_secret, timeout=None, wsdl_version=None):
        ns_client = NetSuiteClient(account=account, timeout=timeout, wsdl_version=wsdl_version)
        ns_client.connect_tba(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            token_key=token_key,
            token_secret=token_secret
        )
        self.client = ns_client
        self.accounts = Accounts(ns_client)
        self.classifications = Classifications(ns_client)
        self.departments = Departments(ns_client)
        self.cost_categories = CostCategory(ns_client)
        self.currencies = Currencies(ns_client)
        self.locations = Locations(ns_client)
        self.vendor_bills = VendorBills(ns_client)
        self.vendors = Vendors(ns_client)
        self.vendor_relationships = VendorSubsidiaryRelationships(ns_client)
        self.subsidiaries = Subsidiaries(ns_client)
        self.journal_entries = JournalEntries(ns_client)
        self.employees = Employees(ns_client)
        self.expense_reports = ExpenseReports(ns_client)
        self.folders = Folders(ns_client)
        self.files = Files(ns_client)
        self.expense_categories = ExpenseCategory(ns_client)
        self.custom_lists = CustomLists(ns_client)
        self.custom_records = CustomRecords(ns_client)
        self.customers = Customers(ns_client)
        self.projects = Projects(ns_client)
        self.vendor_payments = VendorPayments(ns_client)
        self.accountingPeriod = AccountingPeriod(ns_client)
        self.taxType = TaxType(ns_client)
        self.taxGroup = TaxGroup(ns_client)
        self.items = InventoryItem(ns_client)
        self.units = UnitsType(ns_client)
        self.transactions = Transactions(ns_client)
        self.terms = Terms(ns_client)
        self.currencyRate = CurrencyRate(ns_client)
        self.communication = Note(ns_client)
        self.currencyRate = CurrencyRate(ns_client)

        self.ns = ns_client

    def get_record_by_type(self, _type, internal_id):
        return self.ns.RecordRef(type=_type, internalId=internal_id)

    def get_record(self, type_name):
        paginated_search = PaginatedSearch(client=self.ns, type_name=type_name, pageSize=20)
        return paginated_search.records[0]
