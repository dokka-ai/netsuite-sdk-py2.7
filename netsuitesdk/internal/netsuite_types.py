u"""
Declares all NetSuite types which are available through attribute lookup `ns.<type>`
of a :class:`~netsuitesdk.client.NetSuiteClient` instance `ns`.
"""

COMPLEX_TYPES = {
    u'ns0': [
        u'BaseRef',
        u'GetAllRecord',
        u'GetAllResult',
        u'Passport',
        u'RecordList',
        u'RecordRef',
        u'RecordRefList',
        u'InitializeRecord',
        u'InitializeRefList',
        u'InitializeRef',
        u'AttachBasicReference',
        u'ListOrRecordRef',
        u'SearchResult',
        u'SearchStringField',
        u'SearchBooleanField',
        u'SearchDateField',
        u'SearchMultiSelectField',
        u'SearchColumnDoubleField',
        u'SearchColumnSelectField',
        u'SearchColumnDateField',
        u'SearchColumnStringField',
        u'Status',
        u'StatusDetail',
        u'TokenPassport',
        u'TokenPassportSignature',
        u'WsRole',
        u'CustomFieldList',
        u'StringCustomFieldRef',
        u'CustomRecordRef',
        u'SelectCustomFieldRef',
        u'CustomizationRef',
        u'SearchRowBasic',
        u'CustomizationType'
    ],

    # ns4: https://webservices.netsuite.com/xsd/platform/v2017_2_0/messages.xsd
    u'ns4': [
        u'ApplicationInfo',
        u'GetAllRequest',
        u'GetRequest',
        u'GetResponse',
        u'GetAllResponse',
        u'GetListRequest',
        u'GetListResponse',
        u'PartnerInfo',
        u'ReadResponse',
        u'SearchPreferences',
        u'SearchResponse',
        # u'InitializeRefArray',
    ],

    # https://webservices.netsuite.com/xsd/platform/v2017_2_0/common.xsd
    u'ns5': [
        u'AccountSearchBasic',
        u'CustomerSearchBasic',
        u'JobSearchBasic',
        u'LocationSearchBasic',
        u'TransactionSearchBasic',
        u'VendorSearchBasic',
        u'SubsidiarySearchBasic',
        u'EmployeeSearchBasic',
        u'FolderSearchBasic',
        u'FileSearchBasic',
        u'CustomRecordSearchBasic',
        u'CustomListSearchBasic',
        u'AccountingPeriodSearchBasic',
        u'CurrencyRateSearchBasic',
        u'CurrencyRateSearchRowBasic',
        u'ItemSearchBasic',
        u'ItemSearchRowBasic',
        u'AccountSearchRowBasic',
        u'SalesTaxItemSearchRowBasic',
        u'TaxGroupSearchRowBasic',
        u'VendorSearchRowBasic',
        u'ExpenseCategorySearchRowBasic',
        u'UnitsTypeSearchRowBasic',
        u'TransactionSearchRowBasic',
        u'CustomSearchRowBasic',
        u'SubsidiarySearchRowBasic',
        u'VendorSubsidiaryRelationshipSearchBasic',
        u'VendorSubsidiaryRelationshipSearchRowBasic'
    ],

    # urn:relationships.lists.webservices.netsuite.com
    u'ns13': [
        u'Customer', u'CustomerSearch',
        u'Vendor', u'VendorSearch',
        u'Job', u'JobSearch',
        u'VendorSearchAdvanced',
        u'VendorSearchRow',
        u'VendorCurrency',
        u'VendorSubsidiaryRelationship',
        u'VendorSubsidiaryRelationshipSearch',
        u'VendorSubsidiaryRelationshipSearchRow',
        u'VendorSubsidiaryRelationshipSearchAdvanced',
    ],

    # urn:accounting_2017_2.lists.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/lists/v2017_2_0/accounting.xsd
    u'ns17': [
        u'Account', u'AccountSearch',
        u'ExpenseCategory', u'ExpenseCategorySearch',
        u'AccountingPeriod', u'AccountingPeriodSearch',
        u'Classification', u'ClassificationSearch',
        u'Department', u'DepartmentSearch',
        u'Location', u'LocationSearch',
        u'Subsidiary', u'SubsidiarySearch',
        u'VendorCategory', u'VendorCategorySearch',
        u'SalesTaxItem', u'SalesTaxItemSearch',
        u'ItemSearch',
        u'ItemSearchAdvanced',
        u'ItemSearchRow',
        u'UnitsType',
        u'UnitsTypeSearch',
        u'UnitsTypeSearchAdvanced',
        u'UnitsTypeSearchRow',
        u'Term', u'TermSearch',
        u'CurrencyRate',
        u'CurrencyRateSearch',
        u'CurrencyRateSearchRow',
        u'CurrencyRateSearchAdvanced',
        u'AccountSearchAdvanced',
        u'AccountSearchRow',
        u'SalesTaxItemSearchAdvanced',
        u'SalesTaxItemSearchRow',
        u'TaxGroupSearchRow',
        u'TaxGroupSearchAdvanced',
        u'ExpenseCategorySearchRow',
        u'ExpenseCategorySearchAdvanced',
        u'SubsidiarySearchRow',
        u'SubsidiarySearchAdvanced',
    ],

    u'ns19': [
        u'TransactionSearch',
        u'TransactionSearchRow',
        u'TransactionSearchAdvanced',

    ],

    # urn:purchases_2017_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2017_2_0/purchases.xsd
    u'ns21': [
        u'VendorBill',
        u'VendorBillExpense',
        u'VendorBillExpenseList',
        u'VendorBillItem',
        u'VendorBillItemList',
        u'VendorPayment',
        u'VendorPaymentApplyList',
        u'VendorPaymentCredit',
        u'VendorPaymentCreditList',
        u'VendorPaymentApply',
        u'PurchaseOrderItem'
    ],


    # urn:general_2019_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2019_2_0/general.xsd
    u'ns31': [
        u'JournalEntry',
        u'JournalEntryLine',
        u'JournalEntryLineList',

    ],

    u'ns32': [
        u'CustomRecord',
        u'CustomRecordCustomField',
        u'CustomRecordSearch',
        u'CustomListSearch',
        u'CustomRecordType'

    ],

    # https://webservices.netsuite.com/xsd/lists/v2019_2_0/employees.xsd
    u'ns34': [
        u'EmployeeSearch'
    ],

    # urn:employees_2019_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2019_2_0/employees.xsd
    u'ns38': [
        u'ExpenseReport',
        u'ExpenseReportExpense',
        u'ExpenseReportExpenseList',
    ],
    u'ns11': [
        u'FolderSearch',
        u'Folder',
        u'File',
        u'FileSearch',
    ],
}

SIMPLE_TYPES = {
    # ns1: view-source:https://webservices.netsuite.com/xsd/platform/v2017_2_0/coreTypes.xsd
    u'ns1': [
        u'RecordType',
        u'GetAllRecordType',
        u'SearchRecordType',
        u'SearchStringFieldOperator',
        u'GetCustomizationType'

    ],
}
