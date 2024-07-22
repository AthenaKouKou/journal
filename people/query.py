"""
This is our interface to some people data.
"""
# You might need this import:
# import backendcore.data.db_connect as dbc

from backendcore.common.constants import OBJ_ID_NM

from backendcore.data.caching import needs_cache, get_cache

import user_data.users as usrs

from common.common import get_collect_name

import people.roles as rls
from people.fields import (  # noqa 401
    NAME,
    ROLES,
    USER_ID,
)

DB = 'journalDB'
COLLECT = 'people'
CACHE_NM = COLLECT


def needs_people_cache(fn):
    """
    Should be used to decorate any function that uses datacollection methods.
    """
    return needs_cache(fn, CACHE_NM, DB,
                       get_collect_name(COLLECT),
                       key_fld=OBJ_ID_NM,
                       no_id=False)


def is_valid(code):
    people = fetch_dict()
    return code in people


@needs_people_cache
def fetch_list():
    """
    Fetch all people: returns a list
    """
    return get_cache(COLLECT).fetch_list()


@needs_people_cache
def fetch_dict():
    return get_cache(COLLECT).fetch_dict()


@needs_people_cache
def get_choices():
    return get_cache(COLLECT).get_choices()


def fetch_codes():
    """
    Fetch all people codes
    """
    choices = get_choices()
    return list(choices.keys())


@needs_people_cache
def fetch_by_key(_id):
    """
    Get a single entry by term.
    """
    return get_cache(COLLECT).fetch_by_key(_id)


def fetch_all_or_some(name=None, role=None):
    people = fetch_dict()
    if not name or role:
        return people
    else:
        return select(people, name=name, role=role)


def has_role(person, role):
    roles = person.get(ROLES)
    if not roles:
        return False
    return role in roles


def select(people: dict, name=None, role=None):
    """
    Select by name and/or role.
    """
    matches = {}
    for code, person in people.items():
        if name:
            if person.get(NAME) == name:
                matches[person[OBJ_ID_NM]] = people[code]
        elif role:
            if has_role(person, role):
                matches[person[OBJ_ID_NM]] = people[code]
    return matches


def validate_person(person):
    if not person.get(NAME):
        raise ValueError('Every person must have a name.')
    user_id = person.get(USER_ID)
    if user_id:
        # the user_id must actually be in the user collection
        if not usrs.exists(user_id):
            raise ValueError(f'Invalid {user_id=}')


def get_masthead():
    people = fetch_dict()
    masthead = {}
    for role in rls.get_masthead_roles():
        descr = rls.get_descr(role)
        masthead[descr] = []
        for person in people.values():
            if has_role(person, role):
                masthead[descr].append(person.get(NAME))
    return masthead


TEST_ID = 'GC'

TEST_PERSON = {
    OBJ_ID_NM: TEST_ID,
    NAME: 'Callahan le Magnifique',
    USER_ID: 'madeup@utopia.com',
    ROLES: [rls.TEST_ROLE],
}


@needs_people_cache
def add(person: dict):
    validate_person(person)
    return get_cache(COLLECT).add(person)


@needs_people_cache
def delete(_id):
    return get_cache(COLLECT).delete(_id)


@needs_people_cache
def update(_id, person: dict):
    validate_person(person)
    return get_cache(COLLECT).update(_id, person)


def main():
    """
    Run this as a program to see the output formats!
    """
    print("Interactive test of people data module.")
    print(f'{get_masthead()=}')


if __name__ == '__main__':
    main()
