from copy import deepcopy

from unittest.mock import patch

import pytest

import manuscripts.query as qry
from manuscripts.query import (
    REFEREES,
    HISTORY,
)
import manuscripts.states as mst

SOME_BINARY = 'Fake binary value we can fill in if needed'
TEXT_ENTRY_VAL = 'some text'
TEXT_ENTRY_DICT = {qry.TEXT_ENTRY: TEXT_ENTRY_VAL}
NO_TEXT_ENTRY_DICT = {qry.TEXT_ENTRY: ''}


class FakeFileObj():
    def __init__(self, good_file=True):
        if good_file:
            self.filename = FILE_VAL
        else:
            self.filename = BAD_FILE_VAL

    def save(self, filename):
        pass


FILE_VAL = 'some_file.docx'
BAD_FILE_VAL = 'some_file.AVeryBadFileExtension'
MANU_DICT = {qry.MANU_FILE: SOME_BINARY}
FILE_DICT = {qry.MANU_FILE: FakeFileObj(good_file=True)}
NO_FILE_DICT = {}
BAD_FILE_DICT = {qry.MANU_FILE: FakeFileObj(good_file=False)}


def add_test_manuscript():
    sample_dict = deepcopy(qry.TEST_MANU)
    ret = qry.add(sample_dict)
    print(ret)
    return ret


def del_test_entry(_id):
    """
    Delete by id
    """
    return qry.delete(_id)


@pytest.fixture(scope='function')
def temp_manu():
    ret = add_test_manuscript()
    yield ret
    qry.delete(ret)


def test_is_text_entry():
    assert qry.is_text_entry(TEXT_ENTRY_DICT)


def test_is_not_text_entry():
    assert not qry.is_text_entry(NO_TEXT_ENTRY_DICT)


def test_is_file_entry():
    assert qry.is_file_entry(FILE_DICT)


def test_is_not_file_entry():
    assert not qry.is_file_entry(NO_FILE_DICT)


def test_handle_text_entry():
    new_manu_data = qry.handle_text_entry(TEXT_ENTRY_DICT)
    assert new_manu_data[qry.TEXT] == TEXT_ENTRY_VAL
    assert qry.TEXT_ENTRY not in new_manu_data


@patch('manuscripts.query.convert_file', return_value='Text submitted', autospec=True)
def test_handle_file_entry(mock_convert):
    new_manu_data = qry.handle_file_entry(MANU_DICT, FILE_DICT)
    assert new_manu_data[qry.TEXT]
    assert isinstance(new_manu_data[qry.TEXT], str)
    # assert something about the file being on disk somewhere...
    assert qry.FILE not in new_manu_data


def test_handle_file_entry_invalid_file():
    with pytest.raises(ValueError):
        qry.handle_file_entry(MANU_DICT, BAD_FILE_DICT)


def test_add_new_authors():
    pass


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


@patch('people.query.add_role', return_value='Fake ID', autospec=True)
def test_assign_referee(mock_add_role, temp_manu):
    NEW_REF = 'A new referee'
    manu = qry.fetch_by_id(temp_manu)
    refs = manu.get(REFEREES)
    assert NEW_REF not in refs
    qry.assign_referee(temp_manu, referee=NEW_REF)
    manu = qry.fetch_by_id(temp_manu)
    refs = manu.get(REFEREES)
    assert NEW_REF in refs


def test_assign_referee_no_referee(temp_manu):
    with pytest.raises(ValueError):
        qry.assign_referee(temp_manu)


def test_remove_referee_no_referee(temp_manu):
    with pytest.raises(ValueError):
        qry.remove_referee(temp_manu)


def test_remove_referee(temp_manu):
    manu = qry.fetch_by_id(temp_manu)
    print(f'{manu=}')
    old_ref_count = len(manu.get(REFEREES))
    qry.remove_referee(temp_manu, referee=qry.TEST_REFEREE)
    manu = qry.fetch_by_id(temp_manu)
    assert len(manu.get(REFEREES)) < old_ref_count


def test_receive_action(temp_manu):
    new_state = qry.receive_action(temp_manu, mst.TEST_ACTION, **{})
    assert mst.is_valid_state(new_state)


def test_receive_action_bad_manu_id():
    with pytest.raises(ValueError):
        qry.receive_action('bad id', mst.TEST_ACTION, **{})


def test_receive_action_bad_action(temp_manu):
    with pytest.raises(ValueError):
        qry.receive_action(temp_manu, 'bad action', **{})


def test_update_history(temp_manu):
    assert len(qry.fetch_by_id(temp_manu).get(HISTORY, {})) == 1
    qry.update_history(temp_manu, mst.TEST_ACTION, mst.TEST_STATE)
    history = qry.fetch_by_id(temp_manu).get(HISTORY)
    assert len(history) == 2
