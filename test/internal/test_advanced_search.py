import pytest


def test_account_advanced_search(ns_connection):
    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_accounts = list(ns_connection.accounts.advanced_search(
        100, ('internalId', 'name', 'type', ('subsidiary', 'as_list'))))

    all_accounts = list(ns_connection.accounts.get_all_generator(100))
    assert len(advanced_accounts) == len(all_accounts)

    advanced_accounts = sorted(advanced_accounts, key=lambda x: x['internalId'])
    all_accounts = sorted(all_accounts, key=lambda x: x['internalId'])

    for advanced_account, account in zip(advanced_accounts, all_accounts):
        assert advanced_account['internalId'] == account['internalId']
        assert account['acctName'] in advanced_account['name']
        assert advanced_account['type'] == account['acctType']

        subsidiaries = []
        for subsidiary in account['subsidiaryList']['recordRef']:
            subsidiaries.append(subsidiary['internalId'])

        assert sorted(subsidiaries) == advanced_account['subsidiary']


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


def test_items_advanced_search(ns_connection):
    all_items = list(ns_connection.items.get_all())

    ns_connection.client.set_search_preferences(return_search_columns=True)
    advanced_items = list(ns_connection.items.advanced_search(
        100,
        ('internalId', 'expenseAccount', 'class', 'location', 'department',
         'displayName', 'vendorName', 'cost', 'unitsType')
    ))

    assert len(advanced_items) == len(all_items)
    advanced_items = sorted(advanced_items, key=lambda x: x['internalId'])
    all_items = sorted(all_items, key=lambda x: x['internalId'])

    for advanced_item, item in zip(advanced_items, all_items):
        assert advanced_item['internalId'] == item['internalId']
        # assert advanced_item['expenseAccount'] == get_internal_protected(item, 'expenseAccount')
        assert advanced_item['class'] == get_internal_protected(item, 'class')
        assert advanced_item['location'] == get_internal_protected(item, 'location')
        assert advanced_item['department'] == get_internal_protected(item, 'department')
        assert advanced_item['displayName'] == item.get('displayName')
        assert advanced_item['vendorName'] == item.get('vendorName')
        assert advanced_item['cost'] == item.get('cost')
        assert advanced_item['unitsType'] == get_internal_protected(item, 'unitsType')


def test_vendor_advanced_search(ns_connection):
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
