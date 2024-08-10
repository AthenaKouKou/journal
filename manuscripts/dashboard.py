from manuscripts.states import (
    SUBMITTED,
    REFEREE_REVIEW,
    AUTHOR_REVIEW,
    COPY_EDITING,
    FORMATTING,
    PUBLISHED,
    REJECTED,
)

TEXT = 'text'
OPTIONS = 'options'

SUBMITTED_COL_TEXT = 'Submitted'
REFEREE_REVIEW_COL_TEXT = 'With Referees'
COPY_EDITING_COL_TEXT = 'Copy Editing'
AUTHOR_REVIEW_COL_TEXT = 'Awaiting Author Review'
FORMATTING_COL_TEXT = 'Formatting'
PUBLISHED_COL_TEXT = 'Published'

COLUMN_OPTIONS_MAP = {
    SUBMITTED: {
        TEXT: SUBMITTED_COL_TEXT,
        OPTIONS: {
            'Suitable': REFEREE_REVIEW,
            'Desk Reject': REJECTED,
        }
    },
    REFEREE_REVIEW: {
        TEXT: REFEREE_REVIEW_COL_TEXT,
        OPTIONS: {
            'Accept With Revisions': AUTHOR_REVIEW,
            'Accept Without Revisions': COPY_EDITING,
            'Reject': REJECTED,
        }
    },
    AUTHOR_REVIEW: {
        TEXT: AUTHOR_REVIEW_COL_TEXT,
        OPTIONS: {
            'Accept Revisions': COPY_EDITING,
        }
    },
    COPY_EDITING: {
        TEXT: COPY_EDITING_COL_TEXT,
        OPTIONS: {
            'Complete Copy Editing': AUTHOR_REVIEW,
        }
    },
    FORMATTING: {
        TEXT: FORMATTING_COL_TEXT,
        OPTIONS: {
            'Complete Formatting': PUBLISHED,
        }
    },
    PUBLISHED: {
        TEXT: PUBLISHED_COL_TEXT,
        OPTIONS: {
            'Unpublish': FORMATTING,
        }
    },
}

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
