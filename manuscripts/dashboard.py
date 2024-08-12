from manuscripts.query import (STATE_TABLE, SUBMITTED)

COLUMN_OPTIONS_MAP = STATE_TABLE

VALID_COLUMNS = list(COLUMN_OPTIONS_MAP.keys())

TEST_COLUMN = SUBMITTED


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
