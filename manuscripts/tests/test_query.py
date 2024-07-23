from copy import deepcopy

import pytest

import manuscripts.query as qry

import manuscripts.status as mstt

def add_test_sub():
    try:  # in case some failed test left it hanging on...
        qry.delete(qry.TEST_CODE)
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
def temp_sample():
    ret = add_test_sub()
    yield ret
    qry.delete(ret)


def test_add():
    add_test_sub()


def test_fetch_codes(temp_sample):
    codes = qry.fetch_codes()
    assert isinstance(codes, list)


def test_fetch_list(temp_sample):
    samples = qry.fetch_list()
    assert isinstance(samples, list)
    assert len(samples) > 0


def test_fetch_dict(temp_sample):
    samples = qry.fetch_dict()
    assert isinstance(samples, dict)
    assert len(samples) > 0


def test_fetch_by_status_success(temp_sample):
    samples = qry.fetch_by_status(mstt.SUBMITTED)
    assert isinstance(samples, dict)
    assert len(samples) > 0


def test_fetch_by_bad_status(temp_sample):
    with pytest.raises(Exception) as e_info:
        samples = qry.fetch_by_status('pineapple')


# def test_get_choices(temp_sample):
#     choices = qry.get_choices()
#     assert qry.TEST_CODE in choices
