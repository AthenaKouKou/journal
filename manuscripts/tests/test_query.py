from copy import deepcopy

import pytest

import manuscripts.query as qry

import manuscripts.status as mstt

def add_test_sub():
    print(f'{qry.fetch_list()=}')
    try:  # in case some failed test left it hanging on...
        qry.delete(qry.TEST_OBI_ID)
    except Exception:
        print(f'{qry.TEST_CODE} was not present')
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
    qry.delete(qry.TEST_OBJ_ID)


def test_add():
    ret = add_test_sub()
    assert ret
    del_test_entry(qry.TEST_OBJ_ID)


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
    print(qry.fetch_list())
    ret = qry.reset_last_updated(qry.TEST_OBJ_ID)
    assert ret
    print(qry.fetch_list())
    new_updated = qry.fetch_last_updated(qry.TEST_OBJ_ID)
    assert new_updated > qry.TEST_LAST_UPDATED


# def test_get_choices(temp_manuscript):
#     choices = qry.get_choices()
#     assert qry.TEST_CODE in choices
