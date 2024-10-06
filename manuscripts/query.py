"""
This is our interface to our manuscript data.
We never expect our users to add or delete manuscripts,
so we make no provisions for that.
"""
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import pypandoc as pdc

from backendcore.data.caching import needs_cache, get_cache
from backendcore.common.constants import (
    CODE,
    EMAIL,
    NAME,
)
import backendcore.common.time_fmts as tfmt

from journal_common.common import get_collect_name

import people.query as pqry
import people.roles as rls

from manuscripts.fields import (
    ABSTRACT,
    AUTHORS,
    HISTORY,
    LAST_UPDATED,
    OBJ_ID_NM,
    REFEREES,
    STATE,
    TEXT,
    TITLE,
    WCOUNT,
)

from manuscripts.add_form import ( # noqa E402
    FILE,
    MANU_FILE,
    TEXT_ENTRY,
)

import manuscripts.states as mst
from manuscripts.states import (
    ACCEPT,
    ACCEPT_W_REV,
    AUTHOR_REVISIONS,
    ASSIGN_REFEREE,
    AUTHOR_REVIEW,
    COPY_EDITING,
    DONE,
    EDITOR_MOVE,
    EDITOR_REVIEW,
    FORMATTING,
    PUBLISHED,
    REFEREE_REVIEW,
    REJECT,
    REJECTED,
    REMOVE_REFEREE,
    SUBMITTED,
    WITHDRAW, WITHDRAWN,
)


DB = 'journalDB'
COLLECT = 'manuscripts'
CACHE_NM = COLLECT


def needs_manuscripts_cache(fn):
    """
    Should be used to decorate any function that uses datacollection methods.
    """
    return needs_cache(fn, CACHE_NM, DB,
                       get_collect_name(COLLECT),
                       key_fld=OBJ_ID_NM,
                       no_id=False)


@needs_manuscripts_cache
def fetch_list():
    """
    Fetch all manuscripts: returns a list
    """
    return get_cache(COLLECT).fetch_list()


@needs_manuscripts_cache
def fetch_dict():
    return get_cache(COLLECT).fetch_dict()


@needs_manuscripts_cache
def fetch_by_key(manu_id):
    return get_cache(COLLECT).fetch_by_key(manu_id)


@needs_manuscripts_cache
def update_fld(manu_id, fld, val):
    return get_cache(COLLECT).update_fld(manu_id, fld, val, by_id=True)


def fetch_by_id(manu_id):
    return fetch_by_key(manu_id)


def get_last_updated(manu_id):
    if not exists(manu_id):
        raise ValueError(f'No such manuscript id: {manu_id}')
    return fetch_by_id(manu_id).get(LAST_UPDATED, None)


def get_state(manu_id):
    if not exists(manu_id):
        raise ValueError(f'No such manuscript id: {manu_id}')
    return fetch_by_id(manu_id).get(STATE, None)


def exists(code):
    return code in fetch_dict()


TEST_CODE = 'BK'
TEST_LAST_UPDATED = tfmt.datetime_to_iso(tfmt.TEST_OLD_DATETIME)
TEST_REFEREE = 'Kris'

TEST_MANU = {
    ABSTRACT: 'TLDR',
    AUTHORS: [
        {
            NAME: 'Boaz Kaufman',
            EMAIL: 'boaz@donthardcorestrings.com',
        }
    ],
    CODE: TEST_CODE,
    REFEREES: [TEST_REFEREE],
    TEXT: 'When in the course of Boaz events ...',
    TITLE: 'Forays into Kaufman Studies',
    WCOUNT: 500,
}

proj_dir = os.getenv('PROJ_DIR', "")
UPLOAD_DIR = f'{proj_dir}/journal_submissions'
ALLOWED_EXTENSIONS = ['txt', 'docx', 'md', 'html']


def get_valid_exts():
    return ALLOWED_EXTENSIONS


def get_file_ext(filename):
    if '.' not in filename:
        return None
    return filename.rsplit('.', 1)[1].lower()


def is_valid_file(filename):
    return get_file_ext(filename) in get_valid_exts()


TEST_FILE_OBJ = FileStorage(filename=f'good_name.{get_valid_exts()[0]}')


def convert_file(filepath):
    if get_file_ext(filepath) != 'txt':
        output = pdc.convert_file(filepath, 'markdown')
    else:
        with open(filepath, 'r') as f:
            output = '\n'.join(f.readlines())
    return output


def process_file(file):
    output = ''
    if file:
        filename = secure_filename(file.filename)
        if not is_valid_file(filename):
            raise ValueError('Error: valid file types are: '
                             + f'{get_valid_exts()}')
        print(os.path.join(UPLOAD_DIR, filename))
        filepath = os.path.join(UPLOAD_DIR, filename)
        file.save(filepath)
        output = convert_file(filepath)
    return output, filename


def add_file(_id: str, dict_of_files: dict) -> dict:
    if not dict_of_files:
        raise ValueError('Empty dict_of_files dictionary passed.')
    print(f'{dict_of_files=}')
    file_obj = None
    file_obj = dict_of_files.get(MANU_FILE, None)
    if not file_obj:
        raise ValueError('No file in dict_of_files.')
    (text, filename) = process_file(file_obj)
    if filename:
        os.rename(f'{UPLOAD_DIR}/{filename}',
                  f'{UPLOAD_DIR}/{_id}.{get_file_ext(filename)}')
    update(_id, {TEXT: text})
    return (text, filename)


def is_file_entry(manu_data: dict) -> bool:
    return manu_data.get(MANU_FILE)


def set_manuscript_defaults(manu_data):
    manu_data[STATE] = mst.SUBMITTED
    manu_data[LAST_UPDATED] = get_curr_datetime()
    manu_data[TEXT] = manu_data.get(TEXT_ENTRY)


def add_authors(authors: list):
    for author in authors:
        print(f'Adding {author=}')
        pqry.possibly_new_person_add_role(
            author.get(EMAIL),
            rls.AU,
            author.get(NAME)
        )


@needs_manuscripts_cache
def add(manu_data):
    print(f'{manu_data=}')
    set_manuscript_defaults(manu_data)
    add_authors(manu_data[AUTHORS])
    # For testing we may add a manuscript that already has refs!
    if not manu_data.get(REFEREES):
        manu_data[REFEREES] = []
    ret = get_cache(COLLECT).add(manu_data)
    update_history(manu_id=ret,
                   action=SUBMITTED,
                   new_state=SUBMITTED)
    return ret


@needs_manuscripts_cache
def delete(code):
    return get_cache(COLLECT).delete(code, by_id=True)


@needs_manuscripts_cache
def update(code, update_dict):
    return get_cache(COLLECT).update(code, update_dict, by_id=True)


@needs_manuscripts_cache
def fetch_by_state(state: str) -> list:
    if state not in mst.get_valid_states():
        raise ValueError(f'Invalid state: {state}.')
    return get_cache(COLLECT).fetch_by_fld_val(STATE, state)


def get_curr_datetime():
    return tfmt.datetime_to_iso(tfmt.now())


def set_last_updated(manu_id):
    curr_datetime = get_curr_datetime()
    return update_fld(manu_id, LAST_UPDATED, curr_datetime)


def set_state(manu_id, state):
    if state not in mst.get_valid_states():
        raise ValueError(f'Invalid state code {state}. \
        Valid codes are {mst.get_valid_states()}')
    return update(manu_id, {STATE: state})


REFEREE_ARG = 'referee'


def assign_referee(manu_id, **kwargs):
    referee = kwargs.get(REFEREE_ARG)
    if not referee:
        raise ValueError(f'Must provide \'{REFEREE_ARG}\' value to assign a '
                         'referee')
    refs = fetch_by_key(manu_id).get(REFEREES, [])
    refs.append(referee)
    update_fld(manu_id, REFEREES, refs)
    ref = pqry.fetch_by_key(referee)
    try:
        pqry.add_role(ref, 'RE')
    except ValueError as e:
        print(f'Adding referee failed {e}; what should we do here?')
    return REFEREE_REVIEW


def remove_referee(manu_id, **kwargs):
    referee = kwargs.get(REFEREE_ARG)
    if not referee:
        raise ValueError(f'Must provide \'{REFEREE_ARG}\' value to remove a '
                         'referee')
    refs = fetch_by_key(manu_id).get(REFEREES)
    if referee not in refs:
        raise ValueError(f'Referee {referee} not found')
    refs.remove(referee)
    update_fld(manu_id, REFEREES, refs)
    if len(refs) == 0:
        return SUBMITTED
    else:
        return REFEREE_REVIEW


REFEREE_MODIFIED = 'referee_modified'
NEW_STATE = 'new_state'
ACTION = 'action'


def update_history(manu_id: str, action: str, new_state: str, **kwargs):
    history = fetch_by_key(manu_id).get(HISTORY, {})
    history_dict = {}
    history_dict[NEW_STATE] = new_state
    history_dict[ACTION] = action
    for key, value in kwargs.items():
        history_dict[key] = value
    history[get_curr_datetime()] = history_dict
    return update_fld(manu_id, HISTORY, history)


@needs_manuscripts_cache
def update_state(manu_id, state, referee: str = None):
    """
    Updates the history and sets all the new parameters of the manuscript.
    If state is changed to assign_referee or remove_referee the referee
    must also be provided
    """
    if state not in mst.get_valid_states():
        raise ValueError(f'Invalid state code {state}.')
    ret = set_state(manu_id, state)
    update_history(manu_id, state, referee)
    set_last_updated(manu_id)
    return ret


def editor_move(state, **kwargs):
    """
    Forcefully moves the current state to any other state.
    Currently just returns the state passed in, but we may do other things with
    it
    """
    return state


FUNC = 'function'
STATE_MAP = 'state_map'
DESTINATION = 'destination'

COMMON_ACTIONS = {EDITOR_MOVE: {
               FUNC: editor_move,
               },
               WITHDRAW: {
               FUNC: lambda x, **kwargs: WITHDRAWN,
               }}


STATE_TABLE = {
    AUTHOR_REVIEW: {
        DONE: {
            FUNC: lambda x, **kwargs: FORMATTING,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVISIONS: {
        DONE: {
            FUNC: lambda x, **kwargs: EDITOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    COPY_EDITING: {
        DONE: {
            FUNC: lambda x, **kwargs: AUTHOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    EDITOR_REVIEW: {
        ACCEPT: {
            FUNC: lambda x, **kwargs: COPY_EDITING,
        },
        **COMMON_ACTIONS,
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda x, **kwargs: PUBLISHED,
        },
        **COMMON_ACTIONS,
    },
    REFEREE_REVIEW: {
        ACCEPT: {
            FUNC: lambda x, **kwargs: COPY_EDITING,
        },
        ACCEPT_W_REV: {
            FUNC: lambda x, **kwargs: AUTHOR_REVISIONS,
        },
        ASSIGN_REFEREE: {
            FUNC: assign_referee,
        },
        REMOVE_REFEREE: {
            FUNC: remove_referee,
        },
        REJECT: {
            FUNC: lambda x, **kwargs: REJECTED,
        },
        **COMMON_ACTIONS,
    },
    SUBMITTED: {
        REJECT: {
            FUNC: lambda x, **kwargs: REJECTED,
        },
        ASSIGN_REFEREE: {
            FUNC: assign_referee,
        },
        **COMMON_ACTIONS,
    },
}


def receive_action(manu_id, action, **kwargs):
    """
    Currently we have 'referee', 'state' kwargs.
    """
    if not exists(manu_id):
        raise ValueError(f'Invalid manuscript id: {manu_id}')
    if not mst.is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')
    curr_state = get_state(manu_id)
    action_opts = STATE_TABLE[curr_state].get(action, {})
    func = action_opts.get(FUNC, None)
    if func:
        new_state = func(manu_id, **kwargs)
        set_state(manu_id, new_state)
        set_last_updated(manu_id)
        update_history(manu_id=manu_id,
                       action=action,
                       new_state=new_state,
                       **kwargs)
        return new_state
    else:
        raise ValueError(f'Action {action} is invalid in the current state: '
                         f'{curr_state}')


def main():
    """
    Run this as a program to see the output formats!
    """
    print("Interactive test of manuscripts data module.")
    print(f'{fetch_dict()=}')


if __name__ == '__main__':
    main()
