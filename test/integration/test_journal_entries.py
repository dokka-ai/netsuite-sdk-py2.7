import logging
import pytest
import json
import os

logger = logging.getLogger(__name__)

def nottest_get(nc):
    data = next(nc.journal_entries.get_all_generator())
    logger.debug('data = %s', data)
    assert data, 'get all generator didnt work'
    assert data['internalId'] == '16', 'No object found with internalId'

    data = nc.journal_entries.get(externalId='JE_04')
    logger.debug('data = %s', data)
    currency = data['currency']
    assert data, 'No object with externalId'
    assert data['internalId'] == '10512', 'No object with internalId'
    assert data['externalId'] == 'JE_04', 'No object with externalId'
    assert currency['name'] == 'USA', 'Currency does not match'

def nottest_post(nc):
    filename = os.getenv('NS_ACCOUNT').lower() + '.json'
    with open('./test/integration/data/journal_entries/' + filename) as oj:
        s = oj.read()
        je1 = json.loads(s)
    logger.debug('rvb1 = %s', je1)
    res = nc.journal_entries.post(je1)
    logger.debug('res = %s', res)
    assert res['externalId'] == je1['externalId'], 'External ID does not match'
    assert res['type'] == 'journalEntry', 'Type does not match'

    je2 = nc.journal_entries.get(externalId=res['externalId'])
    currency = je2['currency']
    assert je2['internalId'] == '10512', 'No object with internalId'
    assert je2['externalId'] == 'JE_04', 'No object with externalId'
    assert currency['name'] == 'USA', 'Currency does not match'

    logger.debug('je2 = %s', je2)
