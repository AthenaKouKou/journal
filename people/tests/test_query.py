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
    assert qry.has_role(get_person(), rls.TEST_ROLE)


def test_has_role_fake_role():
    assert not qry.has_role(get_person(), 'Not a real role')


def test_has_role_no_role():
    test_person = get_person()
    del test_person[rls.ROLES]
    assert not qry.has_role(test_person, rls.TEST_ROLE)


def test_add_role(temp_person):
    NEW_ROLE = rls.AU
    assert not qry.has_role(qry.fetch_by_key(temp_person), NEW_ROLE)
    qry.add_role(qry.fetch_by_key(temp_person), NEW_ROLE)
    assert qry.has_role(qry.fetch_by_key(temp_person), NEW_ROLE)


def test_add_bad_role(temp_person):
    with pytest.raises(ValueError):
        qry.add_role(qry.fetch_by_key(temp_person), 'Bad role!')


def test_is_editor(temp_person):
    qry.add_role(qry.fetch_by_key(temp_person), rls.ED)
    assert qry.is_editor(temp_person)


def test_is_author(temp_person):
    qry.add_role(qry.fetch_by_key(temp_person), rls.AU)
    assert qry.is_author(temp_person)


def test_is_not_author(temp_person):
    assert qry.is_author(temp_person) == False


def test_is_referee(temp_person):
    qry.add_role(qry.fetch_by_key(temp_person), rls.RE)
    assert qry.is_referee(temp_person)


def test_is_not_referee(temp_person):
    assert qry.is_referee(temp_person) == False


def test_possibly_new_person_add_role_person_exists(temp_person):
    NEW_ROLE = rls.AU
    temp_person_obj = qry.fetch_by_key(temp_person)
    assert not qry.has_role(temp_person_obj, NEW_ROLE)
    new_person = qry.possibly_new_person_add_role(
        temp_person_obj.get(qry.EMAIL),
        NEW_ROLE
    )
    assert qry.has_role(qry.fetch_by_key(new_person), NEW_ROLE)


def test_possibly_new_person_add_role_new_person():
    NEW_ROLE = rls.AU
    new_person = qry.possibly_new_person_add_role(
        get_person().get(qry.EMAIL),
        NEW_ROLE,
        get_person().get(qry.NAME)
    )
    assert qry.fetch_by_key(new_person).get(qry.NAME) == get_person().get(qry.NAME)
    assert qry.has_role(qry.fetch_by_key(new_person), NEW_ROLE)
    del_test_item(new_person)


def test_fetch_by_email(temp_person):
    ret = qry.fetch_by_email(qry.TEST_EMAIL)
    assert isinstance(ret, dict)
    assert ret[qry.EMAIL] == qry.TEST_EMAIL


def test_fetch_by_email_not_there(temp_person):
    assert not qry.fetch_by_email('This email not in db!')


def test_get_masthead(temp_person):
    masthead = qry.get_masthead()
    assert isinstance(masthead, dict)
    for section in masthead.values():
        assert isinstance(section, list)
