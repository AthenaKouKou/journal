from copy import deepcopy

import pytest

import manuscripts.query as qry
from manuscripts.query import (
    REFEREES,
)
import manuscripts.states as mst


def add_test_manuscript():
    sample_dict = deepcopy(qry.TEST_MANU)
    return qry.add(sample_dict)


def del_test_entry(mongo_id):
    """
    Delete by id
    """
    return qry.delete(mongo_id)


@pytest.fixture(scope='function')
def temp_manu():
    ret = add_test_manuscript()
    yield ret
    qry.delete(ret)


def test_add():
    ret = add_test_manuscript()
    assert ret
    del_test_entry(ret)


def test_fetch_list(temp_manu):
    samples = qry.fetch_list()
    assert isinstance(samples, list)
    assert len(samples) > 0


def test_fetch_dict(temp_manu):
    samples = qry.fetch_dict()
    assert isinstance(samples, dict)
    assert len(samples) > 0


def test_fetch_by_state(temp_manu):
    samples = qry.fetch_by_state(mst.TEST_STATE)
    assert isinstance(samples, dict)
    assert len(samples) > 0


def test_fetch_by_bad_state(temp_manu):
    with pytest.raises(Exception):
        qry.fetch_by_state('pineapple')


def test_get_last_updated(temp_manu):
    assert isinstance(qry.get_last_updated(temp_manu), str)


def test_get_last_updated_bad_id():
    with pytest.raises(ValueError):
        qry.get_last_updated('a bad id')


def test_get_state(temp_manu):
    assert qry.get_state(temp_manu) == mst.TEST_STATE


def test_get_state_bad_id():
    with pytest.raises(ValueError):
        qry.get_last_updated('a bad id')


def test_set_last_updated(temp_manu):
    ret = qry.set_last_updated(temp_manu)
    assert ret
    new_updated = qry.get_last_updated(temp_manu)
    assert new_updated > qry.TEST_LAST_UPDATED


def test_assign_referee(temp_manu):
    NEW_REF = 'A new referee'
    manu = qry.fetch_by_id(temp_manu)
    assert len(manu.get(REFEREES)) == 1
    qry.assign_referee(temp_manu, referee=NEW_REF)
    manu = qry.fetch_by_id(temp_manu)
    refs = manu.get(REFEREES)
    assert len(refs) > 1
    assert NEW_REF in refs


def test_assign_referee_no_referee(temp_manu):
    with pytest.raises(ValueError):
        qry.assign_referee(temp_manu)


def test_remove_referee_no_referee(temp_manu):
    with pytest.raises(ValueError):
        qry.remove_referee(temp_manu)


def test_remove_referee(temp_manu):
    manu = qry.fetch_by_id(temp_manu)
    assert len(manu.get(REFEREES)) == 1
    qry.remove_referee(temp_manu, referee=qry.TEST_REFEREE)
    manu = qry.fetch_by_id(temp_manu)
    assert len(manu.get(REFEREES)) == 0


def test_receive_action(temp_manu):
    new_state = qry.receive_action(temp_manu, mst.TEST_ACTION, **{})
    assert mst.is_valid_state(new_state)


def test_receive_action_bad_manu_id():
    with pytest.raises(ValueError):
        qry.receive_action('bad id', mst.TEST_ACTION, **{})


def test_receive_action_bad_action(temp_manu):
    with pytest.raises(ValueError):
        qry.receive_action(temp_manu, 'bad action', **{})
