
def test_call_restlet(ns):
    result = ns.call_get_restlet(9, 1, 'getVendorsCurrencies')
    assert isinstance(result, dict)
    assert result['integrationType'] == 'getVendorsCurrencies'
    assert isinstance(result['data'], dict)


def test_call_restlet_wrong_script(ns):
    result = ns.call_get_restlet(10, 1, 'getVendorsCurrencies')
    assert isinstance(result, dict)
    assert 'error' in result


def test_call_restlet_wrong_deploy(ns):
    result = ns.call_get_restlet(9, 2, 'getVendorsCurrencies')
    assert isinstance(result, dict)
    assert 'error' in result


def test_call_restlet_wrong_integration_type(ns):
    result = ns.call_get_restlet(9, 1, 'getVendorsCurrencies1')
    assert isinstance(result, dict)
    assert result['status'] == 'failed'
    assert not isinstance(result['data'], dict)
