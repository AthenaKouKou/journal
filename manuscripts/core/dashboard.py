from copy import deepcopy

from manuscripts.core.query import (STATE_TABLE, SUBMITTED)
import manuscripts.core.states as st


COLUMN_OPTIONS_MAP = deepcopy(STATE_TABLE)

for state in COLUMN_OPTIONS_MAP:
    for action in COLUMN_OPTIONS_MAP[state]:
        COLUMN_OPTIONS_MAP[state][action] = {}


VALID_COLUMNS = list(COLUMN_OPTIONS_MAP.keys())

TEST_COLUMN = SUBMITTED

COLUMN_ORDER = [st.SUBMITTED, st.REFEREE_REVIEW, st.AUTHOR_REVISIONS,
                st.EDITOR_REVIEW, st.COPY_EDITING, st.AUTHOR_REVIEW,
                st.FORMATTING]


def get_valid_columns() -> list:
    """
    For discovering the names of states.
    """
    return VALID_COLUMNS


def is_valid(candidate: str) -> bool:
    """
    For checking if a state is acceptable.
    """
    return candidate in VALID_COLUMNS


def get_choices():
    return COLUMN_OPTIONS_MAP


def get_choices_order():
    return COLUMN_ORDER
