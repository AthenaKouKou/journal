"""
This is our interface to our manuscript data.
We never expect our users to add or delete manuscripts,
so we make no provisions for that.
"""
from backendcore.data.caching import needs_cache, get_cache
from backendcore.common.constants import CODE
import backendcore.common.time_fmts as tfmt

from journal_common.common import get_collect_name

from manuscripts.fields import (
    ABSTRACT,
    AUTHORS,
    HISTORY,
    LAST_UPDATED,
    OBJ_ID_NM,
    REFEREES,
    STATUS,
    TEXT,
    TITLE,
    WCOUNT,
)

import manuscripts.status as mstt

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


def is_valid(code):
    mans = fetch_dict()
    return code in mans


@needs_manuscripts_cache
def fetch_list():
    """
    Fetch all manuscripts: returns a list
    """
    return get_cache(COLLECT).fetch_list()


@needs_manuscripts_cache
def fetch_dict():
    return get_cache(COLLECT).fetch_dict()


# @needs_manuscripts_cache
# def get_choices():
#     return get_cache(COLLECT).get_choices()


def fetch_codes():
    """
    Fetch all manuscript codes
    """
    manuscripts = fetch_dict()
    return list(manuscripts.keys())


@needs_manuscripts_cache
def fetch_by_id(manu_id):
    return get_cache(COLLECT).fetch_by_key(manu_id)


def fetch_last_updated(manu_id):
    return fetch_by_id(manu_id).get(LAST_UPDATED, None)


TEST_CODE = 'BK'
TEST_LAST_UPDATED = tfmt.datetime_to_iso(tfmt.TEST_OLD_DATETIME)
TEST_REFEREE = 'Kris'

TEST_MANU = {
    ABSTRACT: 'TLDR',
    AUTHORS: ['Boaz Kaufman'],
    CODE: TEST_CODE,
    LAST_UPDATED: TEST_LAST_UPDATED,
    REFEREES: [TEST_REFEREE],
    STATUS: mstt.SUBMITTED,
    TEXT: 'When in the course of Boaz events it becomes necessary...',
    TITLE: 'Forays into Kaufman Studies',
    WCOUNT: 500,
}


@needs_manuscripts_cache
def add(manu_dict):
    manu_dict[STATUS] = mstt.SUBMITTED
    return get_cache(COLLECT).add(manu_dict)


@needs_manuscripts_cache
def delete(code):
    return get_cache(COLLECT).delete(code, by_id=True)


@needs_manuscripts_cache
def update(code, update_dict):
    return get_cache(COLLECT).update(code, update_dict, by_id=True)


@needs_manuscripts_cache
def fetch_by_status(status_code):
    if status_code not in mstt.get_valid_statuses():
        raise ValueError(f'Invalid status code {status_code}. \
        Valid codes are {mstt.get_valid_statuses}')
    return get_cache(COLLECT).fetch_by_fld_val(STATUS, status_code)


def get_curr_datetime():
    return tfmt.datetime_to_iso(tfmt.now())


@needs_manuscripts_cache
def reset_last_updated(manu_id):
    curr_datetime = get_curr_datetime()
    return get_cache(COLLECT).update_fld(manu_id, LAST_UPDATED, curr_datetime,
                                         by_id=True)


@needs_manuscripts_cache
def set_status(manu_id, status_code):
    if status_code not in mstt.get_valid_statuses():
        raise ValueError(f'Invalid status code {status_code}. \
        Valid codes are {mstt.get_valid_statuses}')
    return get_cache(COLLECT).update(manu_id,
                                     {STATUS: status_code},
                                     by_id=True)


@needs_manuscripts_cache
def assign_referee(manu_id, referee: str):
    refs = get_cache(COLLECT).fetch_by_key(manu_id).get(REFEREES, [])
    refs.append(referee)
    return get_cache(COLLECT).update_fld(manu_id, REFEREES, refs, by_id=True)


@needs_manuscripts_cache
def remove_referee(manu_id, referee: str):
    refs = get_cache(COLLECT).fetch_by_key(manu_id).get(REFEREES)
    refs.remove(referee)
    return get_cache(COLLECT).update_fld(manu_id, REFEREES, refs, by_id=True)


REFEREE_MODIFIED = 'referee_modified'
NEW_STATUS = 'new_status'


@needs_manuscripts_cache
def update_history(manu_id, status_code, referee: str = None):
    history = get_cache(COLLECT).fetch_by_key(manu_id).get(HISTORY, {})
    history_dict = {}
    history_dict[NEW_STATUS] = status_code
    history[get_curr_datetime()] = history_dict
    return get_cache(COLLECT).update_fld(manu_id, HISTORY, history, by_id=True)


@needs_manuscripts_cache
def update_status(manu_id, status_code, referee: str = None):
    """
    Updates the history and sets all the new parameters of the manusccript.
    If status is changed to assign_referee or remove_referee the referee
    must also be provided
    """
    if status_code not in mstt.get_valid_statuses():
        raise ValueError(f'Invalid status code {status_code}. \
        Valid codes are {mstt.get_valid_statuses}')
    ret = set_status(manu_id, status_code)
    update_history(manu_id, status_code, referee)
    reset_last_updated(manu_id)
    return ret


def main():
    """
    Run this as a program to see the output formats!
    """
    print("Interactive test of manuscripts data module.")
    print(f'{fetch_dict()=}')


if __name__ == '__main__':
    main()
