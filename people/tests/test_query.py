from copy import deepcopy

from unittest.mock import patch

import pytest

import people.query as qry
import people.roles as rls


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
    ret = add_test_person()
    yield ret
    del_test_item(ret)


@pytest.fixture(scope='function')
def new_person():
    """
    Creates an entry, but does not delete it after test runs.
    """
    return add_test_person()


def test_fetch_codes(temp_person):
    codes = qry.fetch_codes()
    assert isinstance(codes, list)
    assert temp_person in codes


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
    assert temp_person in choices


def test_fetch_by_key(temp_person):
    entry = qry.fetch_by_key(temp_person)
    assert entry[qry.OBJ_ID_NM] == temp_person


def test_fetch_by_key_not_there():
    assert qry.fetch_by_key('A Very Unlikely Term') is None


def test_add():
    qry.add(get_person())
    obj_id = qry.fetch_list()[0].get(qry.OBJ_ID_NM)
    assert qry.fetch_by_key(obj_id) is not None
    del_test_item(obj_id)


def test_add_no_name():
    person = get_nameless_person()
    with pytest.raises(ValueError):
        qry.add(person)


def test_delete(new_person):
    qry.delete(new_person)
    assert qry.fetch_by_key(new_person) is None


def test_delete_not_there():
    with pytest.raises(ValueError):
        qry.delete('not an existing code')


def test_update(temp_person):
    NEW_NAME = 'A new name'
    update_dict = {qry.NAME: NEW_NAME}
    assert qry.fetch_by_key(temp_person)[qry.NAME] != NEW_NAME
    qry.update(temp_person, update_dict)
    assert qry.fetch_by_key(temp_person)[qry.NAME] == NEW_NAME


def test_update_not_there():
    update_dict = {qry.NAME: 'something'}
    with pytest.raises(ValueError):
        qry.update('not an existing code', update_dict)


def test_update_no_name(temp_person):
    person = get_nameless_person()
    with pytest.raises(ValueError):
        qry.update(temp_person, person)


def test_has_role():
    assert qry.has_role(qry.TEST_PERSON, rls.TEST_ROLE)


def test_has_role_no_role():
    BAD_ROLE = 'PU'
    assert not qry.has_role(qry.TEST_PERSON, BAD_ROLE)


def test_add_role(temp_person):
    NEW_ROLE = rls.AU
    assert not qry.has_role(qry.fetch_by_key(temp_person), NEW_ROLE)
    qry.add_role(qry.fetch_by_key(temp_person), NEW_ROLE)
    assert qry.has_role(qry.fetch_by_key(temp_person), NEW_ROLE)


def test_get_masthead(temp_person):
    masthead = qry.get_masthead()
    assert isinstance(masthead, dict)
    for section in masthead.values():
        assert isinstance(section, list)
