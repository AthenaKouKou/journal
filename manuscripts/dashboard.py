from manuscripts.status import (
    SUBMITTED,
    UNDER_REFEREE,
    AUTHOR_REVISION,
    COPY_EDITING,
    AUTHOR_REVIEW,
    FORMATTING,
    PUBLISHED,
    REFEREE_REJECTED,
)

TEXT = 'text'
OPTIONS = 'options'

SUBMITTED_COL_TEXT = 'Submitted'
UNDER_REFEREE_COL_TEXT = 'With Referees'
AUTHOR_REVISION_COL_TEXT = 'Needs Author Revision'
COPY_EDITING_COL_TEXT = 'Copy Editing'
AUTHOR_REVIEW_COL_TEXT = 'Awaiting Author Approval'
FORMATTING_COL_TEXT = 'Formatting'
PUBLISHED_COL_TEXT = 'Published'

COLUMN_OPTIONS_MAP = {
    SUBMITTED: {
        TEXT: SUBMITTED_COL_TEXT,
        OPTIONS: {
            'Suitable': UNDER_REFEREE,
            'Desk Reject': REFEREE_REJECTED,
        }
    },
    UNDER_REFEREE: {
        TEXT: UNDER_REFEREE_COL_TEXT,
        OPTIONS: {
            'Accept With Revisions': AUTHOR_REVISION,
            'Accept Without Revisions': COPY_EDITING,
            'Reject': REFEREE_REJECTED,
        }
    },
    AUTHOR_REVISION: {
        TEXT: AUTHOR_REVISION_COL_TEXT,
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
    AUTHOR_REVIEW: {
        TEXT: AUTHOR_REVIEW_COL_TEXT,
        OPTIONS: {
            'Complete Author Approval': FORMATTING,
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
    For discovering the names of statuses.
    """
    return VALID_COLUMNS


def is_valid(candidate: str) -> bool:
    """
    For checking if a status is acceptable.
    """
    return candidate in VALID_COLUMNS


def get_choices():
    return COLUMN_OPTIONS_MAP
