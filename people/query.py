"""
This is our interface to journal people data.
"""
from backendcore.common.constants import OBJ_ID_NM
from backendcore.data.caching import needs_cache, get_cache

from journal_common.common import get_collect_name

import people.roles as rls
from people.fields import (  # noqa 401
    BIO,
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


def person_to_masthead(person: dict) -> dict:
    mast_peep = {}
    mast_peep[NAME] = person.get(NAME, '')
    mast_peep[BIO] = person.get(BIO, '')
    return mast_peep


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
    if name or role:
        return select(people, name=name, role=role)
    else:
        return people


def has_role(person, role):
    roles = person.get(ROLES)
    if not roles:
        return False
    return role in roles


def add_role(person, role):
    if not person or not role:
        return
    if has_role(person, role):
        return
    person[ROLES].append(role)
    id = person['_id']
    del person['_id']
    update(id, person)
    return person


def select(people: dict, name=None, role=None):
    """
    Select by name or role.
    """
    matches = {}
    for code, person in people.items():
        if name:
            if person.get(NAME) == name:
                matches[person[OBJ_ID_NM]] = people[code]
        elif role:
            print(f'{role=}')
            if has_role(person, role):
                matches[person[OBJ_ID_NM]] = people[code]
    return matches


def fetch_by_id(id=None):
    """
    Fetch a person by user_id (currently different from document id).
    """
    people = fetch_dict()
    for code, person in people.items():
        if id:
            if person.get(USER_ID):
                return people[code]
    return {}


def validate_person(person):
    if not person.get(NAME):
        raise ValueError('Every person must have a name.')


def get_masthead():
    people = fetch_dict()
    masthead = {}
    for role in rls.get_masthead_roles():
        descr = rls.get_descr(role)
        masthead[descr] = []
        for person in people.values():
            if has_role(person, role):
                mast_peep = person_to_masthead(person)
                masthead[descr].append(mast_peep)
    return masthead


TEST_PERSON = {
    NAME: 'Callahan le Magnifique',
    USER_ID: 'madeup@utopia.com',
    ROLES: [rls.TEST_ROLE],
    BIO: 'Un homme tres magnifique',
}


@needs_people_cache
def add(person: dict):
    validate_person(person)
    return get_cache(COLLECT).add(person)


@needs_people_cache
def delete(_id):
    return get_cache(COLLECT).delete(_id, by_id=True)


@needs_people_cache
def update(_id, person: dict):
    validate_person(person)
    return get_cache(COLLECT).update(_id, person, by_id=True)


def main():
    """
    Run this as a program to see the output formats!
    """
    print("Interactive test of people data module.")
    print(f'{get_masthead()=}')


if __name__ == '__main__':
    main()
