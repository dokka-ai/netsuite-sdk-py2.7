import logging
import pytest
import zeep

logger = logging.getLogger(__name__)

@pytest.mark.parametrize('type_name', ['currency'])
def test_get_all(ns, type_name):
    records = ns.getAll(recordType=type_name)
    assert len(records) > 0, 'No records of type {} returned'.format(type_name)

@pytest.mark.parametrize('type_name', ['account', 'vendor', 'department', 'location', 'classification', 'subsidiaries', 'employees'])
def test_get_all_not_supported(ns, type_name):
    with pytest.raises(zeep.exceptions.Fault) as ex:
        records = ns.getAll(recordType=type_name)
    assert 'is not a legal value' in str(ex.value)
