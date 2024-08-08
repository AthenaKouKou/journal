from copy import deepcopy

import pytest

import manuscripts.query as qry
from manuscripts.query import (
    OBJ_ID_NM,
    REFEREES,
)

import manuscripts.status as mstt


def add_test_sub():
    sample_dict = deepcopy(qry.TEST_MANU)
    return qry.add(sample_dict)


def del_test_entry(mongo_id):
    """
    Delete by id
    """
    return qry.delete(mongo_id)


@pytest.fixture(scope='function')
def temp_manuscript():
    ret = add_test_sub()
    yield ret
    qry.delete(ret)


def test_add():
    ret = add_test_sub()
    obj_id = qry.fetch_list()[0].get(OBJ_ID_NM)
    assert ret
    del_test_entry(obj_id)


def test_fetch_codes(temp_manuscript):
    codes = qry.fetch_codes()
    assert isinstance(codes, list)


def test_fetch_list(temp_manuscript):
    samples = qry.fetch_list()
    assert isinstance(samples, list)
    assert len(samples) > 0


def test_fetch_dict(temp_manuscript):
    samples = qry.fetch_dict()
    assert isinstance(samples, dict)
    assert len(samples) > 0


def test_fetch_by_status_success(temp_manuscript):
    samples = qry.fetch_by_status(mstt.SUBMITTED)
    assert isinstance(samples, dict)
    assert len(samples) > 0


def test_fetch_by_bad_status(temp_manuscript):
    with pytest.raises(Exception) as e_info:
        samples = qry.fetch_by_status('pineapple')


def test_reset_last_updated(temp_manuscript):
    ret = qry.reset_last_updated(temp_manuscript)
    assert ret
    new_updated = qry.fetch_last_updated(temp_manuscript)
    assert new_updated > qry.TEST_LAST_UPDATED


# def test_get_choices(temp_manuscript):
#     choices = qry.get_choices()
#     assert qry.TEST_CODE in choices


def test_assign_referee(temp_manuscript):
    manu = qry.fetch_by_id(temp_manuscript)
    assert len(manu.get(REFEREES)) == 1
    qry.assign_referee(temp_manuscript, 'A new referee')
    manu = qry.fetch_by_id(temp_manuscript)
    assert len(manu.get(REFEREES)) > 1


def test_assign_referee(temp_manuscript):
    manu = qry.fetch_by_id(temp_manuscript)
    assert len(manu.get(REFEREES)) == 1
    qry.remove_referee(temp_manuscript, qry.TEST_REFEREE)
    manu = qry.fetch_by_id(temp_manuscript)
    assert len(manu.get(REFEREES)) == 0
