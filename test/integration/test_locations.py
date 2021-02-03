import logging
import pytest

logger = logging.getLogger(__name__)

def test_get(nc):
    data = nc.locations.get_all()
    logger.debug('data = %s', data)
    assert data, 'get all didnt work'

    internal_id = data[0]['internalId']
    data = nc.locations.get(internalId=internal_id)
    logger.debug('data = %s', data)
    assert data, 'No object with internalId {}'.format(internal_id)

def test_post(nc):
    data = {}
    with pytest.raises(NotImplementedError) as ex:
        nc.locations.post(data)
