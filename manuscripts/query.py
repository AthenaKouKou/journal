"""
This is our interface to our us manuscript data.
We never expect our users to add or delete manuscripts,
so we make no provisions for that.
"""
# import backendcore.data.db_connect as dbc

from backendcore.data.caching import needs_cache, get_cache

from backendcore.common.constants import (
    CODE,
)

from common.common import get_collect_name

from manuscripts.fields import (
    TITLE,
    WCOUNT,
    AUTHORS,
    TEXT_ENTRY,
    # TEXT_FILE,
    ABSTRACT,
    OBJ_ID_NM,
    STATUS,
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


"""
These should get tests, since the editor will use them.
"""
TEST_CODE = 'BK'

TEST_MANU = {
    CODE: TEST_CODE,
    TITLE: 'Forays into Kaufman Studies',
    WCOUNT: 500,
    AUTHORS: ['Boaz Kaufman'],
    TEXT_ENTRY: 'When in the course of Boaz events it becomes necessary...',
    ABSTRACT: 'TLDR',
    STATUS: mstt.SUBMITTED,
}


@needs_manuscripts_cache
def add(manuscripts_dict):
    return get_cache(COLLECT).add(manuscripts_dict)


@needs_manuscripts_cache
def delete(reg_code):
    return get_cache(COLLECT).delete(reg_code)


@needs_manuscripts_cache
def update(code, update_dict):
    return get_cache(COLLECT).update(code, update_dict)


@needs_manuscripts_cache
def fetch_by_status(status_code):
    if status_code not in mstt.get_valid_statuses():
        raise ValueError(f'Invalid status code {status_code}. \
        Valid codes are {mstt.get_valid_statuses}')
    return get_cache(COLLECT).fetch_by_fld_val(STATUS, status_code)


@needs_manuscripts_cache
def set_status(manu_id, status_code):
    if status_code not in mstt.get_valid_statuses:
        raise ValueError(f'Invalid status code {status_code}. \
        Valid codes are {mstt.get_valid_statuses}')
    return get_cache(COLLECT).update(manu_id,
                                     {STATUS: status_code},
                                     by_id=True)


def main():
    """
    Run this as a program to see the output formats!
    """
    print("Interactive test of manuscripts data module.")
    print(f'{fetch_dict()=}')


if __name__ == '__main__':
    main()
