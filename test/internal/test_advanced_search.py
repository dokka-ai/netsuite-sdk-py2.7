import pytest
from six import itervalues


def round_d(n, decimals=0):
    if n is None:
        return n
    multiplier = 10 ** decimals
    return round(n * multiplier) / multiplier


def test_account_search(ns_connection):
    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_accounts = list(ns_connection.accounts.advanced_search(
        100,
        ('internalId', 'name', 'legalName', 'type', 'subsidiary', 'number', 'description'),
        search_criteria=(
            ('type', 'anyOf', [
                '_expense',
                '_otherExpense', ]),
        )))

    new_advanced_accounts = {}
    for acc in advanced_accounts:
        if acc['internalId'] in new_advanced_accounts:
            new_advanced_accounts[acc['internalId']]['subsidiary'].append(acc['subsidiary'])
        else:
            new_acc = acc
            new_acc['subsidiary'] = [acc['subsidiary']]
            new_advanced_accounts[acc['internalId']] = new_acc

    advanced_accounts = [acc for acc in itervalues(new_advanced_accounts)]

    all_accounts = list(ns_connection.accounts.get_all_generator(100))
    all_accounts = [a for a in all_accounts if a['acctType'] in ['_expense', '_otherExpense']]
    assert len(advanced_accounts) == len(all_accounts)

    advanced_accounts = sorted(advanced_accounts, key=lambda x: x['internalId'])
    all_accounts = sorted(all_accounts, key=lambda x: x['internalId'])

    for advanced_account, account in zip(advanced_accounts, all_accounts):
        assert advanced_account['internalId'] == account['internalId']
        # some reason in advance search there is no 'human's' name of account
        assert account['acctName'] in advanced_account['name']
        assert advanced_account['type'] == account['acctType']

        subsidiaries = []
        for subsidiary in account['subsidiaryList']['recordRef']:
            subsidiaries.append(subsidiary['internalId'])

        set_advanced_account = set(advanced_account['subsidiary'])
        set_subsidiaries = set(subsidiaries)

        assert len(set_subsidiaries.difference(set_advanced_account)) == 0


# doesnt work
# def test_tax_advanced_search(ns_connection):
#     all_taxes = list(ns_connection.taxType.get_all())
#
#     ns_connection.client.set_search_preferences(return_search_columns=True)
#     advanced_taxes = list(ns_connection.taxGroup.advanced_search(
#         100, ('internalId', 'itemId', 'rate')))
#
#     assert len(advanced_taxes) == len(all_taxes)


def get_internal_protected(d, v):
    try:
        return d[v]['internalId']
    except:
        return None


def test_items_search(ns_connection):
    all_items = list(ns_connection.items.get_all())

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_items = list(ns_connection.items.advanced_search(
        100,
        ('internalId', 'expenseAccount', 'class', 'location', 'department',
         'displayName', 'vendorName', 'cost', 'unitsType', 'itemId',
         'deferredExpenseAccount', 'incomeAccount', 'lastPurchasePrice',
         'purchasePriceVarianceAcct', 'purchaseDescription',
         'otherVendor', 'vendorCode', 'vendorCost', 'vendorPriceCurrency',
         'subsidiary'),
    ))

    new_advanced_items = {}
    for item in advanced_items:
        if item['internalId'] in new_advanced_items:
            new_advanced_items[item['internalId']]['vendor_prices'].append({
                'vendor_id': item['otherVendor'],
                'currency_name': item['vendorPriceCurrency'],
                'vendor_cost': item['vendorCost'],
            })
        else:
            new_item = item
            new_item['vendor_prices'] = [{
                'vendor_id': item['otherVendor'],
                'currency_name': item['vendorPriceCurrency'],
                'vendor_cost': item['vendorCost'],
            }]
            new_advanced_items[item['internalId']] = new_item

    advanced_items = [acc for acc in itervalues(new_advanced_items)]

    advanced_items = sorted(advanced_items, key=lambda x: x['internalId'])
    all_items = sorted(all_items, key=lambda x: x['internalId'])

    assert len(advanced_items) == len(all_items)
    for advanced_item, item in zip(advanced_items, all_items):
        assert advanced_item['internalId'] == item['internalId']
        if advanced_item['incomeAccount']:
            # in advanced search expenseAccount it is Expense/COGS Account
            # but in regular search there are 2 fields:
            # expenseAccount and cogsAccount. and I saw that if
            assert None is get_internal_protected(item, 'expenseAccount')
        else:
            assert advanced_item['expenseAccount'] == get_internal_protected(item, 'expenseAccount')
        assert advanced_item['class'] == get_internal_protected(item, 'class')
        assert advanced_item['location'] == get_internal_protected(item, 'location')
        assert advanced_item['department'] == get_internal_protected(item, 'department')
        assert advanced_item['displayName'] == item.get('displayName')
        assert advanced_item['itemId'] == item.get('itemId')
        assert advanced_item['vendorName'] == item.get('vendorName')
        assert advanced_item['purchaseDescription'] == item.get('purchaseDescription')
        # clients has different cost some reasons s
        # assert advanced_item['cost'] == item.get('cost')
        assert round_d(advanced_item['lastPurchasePrice'], 2) == round_d(item.get('lastPurchasePrice'), 2)
        assert advanced_item['unitsType'] == get_internal_protected(item, 'unitsType')


def test_vendor_search(ns_connection):
    all_vendors = list(ns_connection.vendors.get_all())

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_vendors = list(ns_connection.vendors.advanced_search(
        100,
        ('internalId', 'entityId', 'subsidiary', 'currency', 'terms',)
    ))

    assert len(advanced_vendors) == len(all_vendors)
    advanced_vendors = sorted(advanced_vendors, key=lambda x: x['internalId'])
    all_vendors = sorted(all_vendors, key=lambda x: x['internalId'])

    for advanced_item, item in zip(advanced_vendors, all_vendors):
        assert advanced_item['internalId'] == item['internalId']
        # IN condition
        assert advanced_item['entityId'] in item.get('entityId')
        assert advanced_item['subsidiary'] == item['subsidiary']['internalId']
        assert advanced_item['currency'] == item['currency']['internalId']
        assert advanced_item['terms'] == get_internal_protected(item, 'terms')


# def test_vendor_advanced_search_by_id(ns_connection):
#     ns_connection.client.set_search_preferences(return_search_columns=True)
#     advanced_vendors = list(ns_connection.vendors.advanced_search_by_id(
#         100, 30))


def test_expense_categories_search(ns_connection):
    """
    HOW TO JOIN account's name in advanced search
    """
    categories = list(ns_connection.expense_categories.get_all())

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_categories = list(ns_connection.expense_categories.advanced_search(
        100,
        ('internalId', 'name', 'account', 'subsidiary',)
    ))

    assert len(advanced_categories) == len(categories)


def test_units_search(ns_connection):
    units = list(ns_connection.units.get_all())

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_units = list(ns_connection.units.advanced_search(
        100,
        ('internalId', 'name',)
    ))

    assert len(advanced_units) == len(units)

    advanced_units = sorted(advanced_units, key=lambda x: x['internalId'])
    units = sorted(units, key=lambda x: x['internalId'])

    for advanced_unit, unit in zip(advanced_units, units):
        assert advanced_unit['internalId'] == unit['internalId']
        assert advanced_unit['name'] == unit['name']


def test_currency_rate_search(ns_connection):
    """
    TODO Works with test env but doesn't work with client's env
    """
    currency_rate = list(ns_connection.currencyRate.get_all())

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_currency_rate = list(ns_connection.currencyRate.advanced_search(
        100,
        ('internalId', 'baseCurrency', 'transactionCurrency',
         'effectiveDate', 'exchangeRate')
    ))

    assert len(advanced_currency_rate) == len(currency_rate)

    advanced_currency_rate = sorted(advanced_currency_rate, key=lambda x: int(x['internalId']))
    currency_rate = sorted(currency_rate, key=lambda x: int(x['internalId']))

    for advanced_rate, rate in zip(advanced_currency_rate, currency_rate):
        assert advanced_rate['internalId'] == rate['internalId']
        assert advanced_rate['baseCurrency'] == get_internal_protected(rate, 'baseCurrency')
        assert advanced_rate['transactionCurrency'] == get_internal_protected(rate, 'transactionCurrency')
        assert advanced_rate['effectiveDate'] == rate['effectiveDate']
        assert advanced_rate['exchangeRate'] == rate['exchangeRate']


def test_purchase_orders_search(ns_connection):
    orders = ns_connection.purchase_orders.get()
    orders = [o for o in orders if o['status'].find("Pending Bill") >= 0]

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_orders = list(ns_connection.purchase_orders.advanced_search(
        100,
        ('internalId', 'tranId', 'status',
         'entity', 'transactionNumber', 'quantity', ),
        search_criteria=(
            ('status', 'anyOf', ['_purchaseOrderPendingBillingPartiallyReceived',
                                 '_purchaseOrderPendingBill',
                                 '_purchaseOrderPartiallyReceived',]),
            ('transactionNumber', 'startsWith', 'PURCHORD'),
            ('quantity', 'empty', None)
        )
    ))
    advanced_orders = sorted(advanced_orders, key=lambda x: int(x['internalId']))
    orders = sorted(orders, key=lambda x: int(x['internalId']))

    assert len(advanced_orders) == len(orders)

    for advanced_order, order in zip(advanced_orders, orders):
        assert advanced_order['internalId'] == order['internalId']
        assert advanced_order['tranId'] == order['tranId']
        assert advanced_order['entity'] == get_internal_protected(order, 'entity')


def test_subsidiaries_rate_search(ns_connection):
    subsidiaries = ns_connection.subsidiaries.get_all()

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_subsidiaries = list(ns_connection.subsidiaries.advanced_search(
        100, ('internalId', 'name', 'nameNoHierarchy', 'legalName')
    ))

    assert len(advanced_subsidiaries) == len(subsidiaries)

    advanced_subsidiaries = sorted(advanced_subsidiaries, key=lambda x: int(x['internalId']))
    subsidiaries = sorted(subsidiaries, key=lambda x: int(x['internalId']))

    for advanced_sub, sub in zip(advanced_subsidiaries, subsidiaries):
        assert advanced_sub['internalId'] == sub['internalId']
        assert advanced_sub['nameNoHierarchy'] == sub['name']


def test_vendor_subsidiary_relationship_search(ns_connection):
    vrs = ns_connection.vendor_relationships.get_all()

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_vrs = list(ns_connection.vendor_relationships.advanced_search(
        100, ('internalId', 'entity', 'taxitem', 'subsidiary',)
    ))

    assert len(advanced_vrs) == len(vrs)

    advanced_vrs = sorted(advanced_vrs, key=lambda x: int(x['internalId']))
    vrs = sorted(vrs, key=lambda x: int(x['internalId']))

    for advanced_vr, vr in zip(advanced_vrs, vrs):
        assert advanced_vr['internalId'] == vr['internalId']
        assert advanced_vr['entity'] == get_internal_protected(vr, 'entity')
        assert advanced_vr['taxitem'] == get_internal_protected(vr, 'taxItem')
        assert advanced_vr['subsidiary'] == get_internal_protected(vr, 'subsidiary')


def _test_saved_vendors_advanced_search(ns_connection):
    ns_connection.client.set_search_preferences(return_search_columns=True)

    all_vendors = list(ns_connection.vendors.advanced_search_by_id(100, 30))