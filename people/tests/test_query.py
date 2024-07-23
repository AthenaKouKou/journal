from copy import deepcopy

from unittest.mock import patch

import pytest

import people.query as qry


def del_test_item(code):
    """
    Delete by code.
    """
    return qry.delete(code)


def get_person():
    return deepcopy(qry.TEST_PERSON)


def get_nameless_person():
    person = get_person()
    del person[qry.NAME]
    return person


def add_test_person():
    return qry.add(get_person())


@pytest.fixture(scope='function')
def temp_person():
    try:  # in case some failed test left it hanging on...
        del_test_item(qry.TEST_ID)
    except Exception:
        print(f'{qry.TEST_ID} was not present')
    ret = add_test_person()
    yield ret
    del_test_item(qry.TEST_ID)


@pytest.fixture(scope='function')
def new_person():
    """
    Creates an entry, but does not delete it after test runs.
    """
    return add_test_person()


def test_fetch_codes(temp_person):
    codes = qry.fetch_codes()
    assert isinstance(codes, list)
    assert qry.TEST_ID in codes


def test_fetch_list(temp_person):
    persons = qry.fetch_list()
    assert isinstance(persons, list)
    assert len(persons) > 0


def test_fetch_dict(temp_person):
    persons = qry.fetch_dict()
    assert isinstance(persons, dict)
    assert len(persons) > 0


def test_get_choices(temp_person):
    choices = qry.get_choices()
    assert qry.TEST_ID in choices


def test_fetch_by_key(temp_person):
    entry = qry.fetch_by_key(qry.TEST_ID)
    assert entry[qry.OBJ_ID_NM] == qry.TEST_ID


def test_fetch_by_key_not_there():
    assert qry.fetch_by_key('A Very Unlikely Term') is None


def test_add():
    qry.add(get_person())
    assert qry.fetch_by_key(qry.TEST_ID) is not None
    del_test_item(qry.TEST_ID)


def test_add_no_name():
    person = get_nameless_person()
    with pytest.raises(ValueError):
        qry.add(person)


def test_delete(new_person):
    qry.delete(qry.TEST_ID)
    assert qry.fetch_by_key(qry.TEST_ID) is None


def test_delete_not_there():
    with pytest.raises(ValueError):
        qry.delete('not an existing code')


def test_update(temp_person):
    NEW_NAME = 'A new name'
    update_dict = {qry.NAME: NEW_NAME}
    assert qry.fetch_by_key(qry.TEST_ID)[qry.NAME] != NEW_NAME
    qry.update(qry.TEST_ID, update_dict)
    assert qry.fetch_by_key(qry.TEST_ID)[qry.NAME] == NEW_NAME


def test_update_not_there():
    update_dict = {qry.NAME: 'something'}
    with pytest.raises(ValueError):
        qry.update('not an existing code', update_dict)


def test_update_no_name(temp_person):
    person = get_nameless_person()
    with pytest.raises(ValueError):
        qry.update(qry.TEST_ID, person)


def test_get_masthead(temp_person):
    masthead = qry.get_masthead()
    assert isinstance(masthead, dict)
    for section in masthead.values():
        assert isinstance(section, list)
