from journal.manuscripts.status import (
    SUBMITTED,
    UNDER_REFEREE,
    AUTHOR_REVISION,
    COPY_EDITING,
    AUTHOR_REVIEW,
    FORMATTING,
    PUBLISHED,
    REFEREE_REJECTED,
)

stt_ep = '/Journal/manuscripts/status/edit'
# ^ This shouldn't be hardcoded but I'd like the Options to have the link
# to the status update endpoint. Getting the proper ep from endpoints.py
# means a circular import. So here we are. - Boaz
TEXT = 'text'
OPTIONS = 'options'

SUBMITTED_COL_TEXT = 'Submitted'
UNDER_REFEREE_COL_TEXT = 'With Referees'
AUTHOR_REVISION_COL_TEXT = 'Needs Author Revision'
COPY_EDITING_COL_TEXT = 'Copy Editing'
AUTHOR_REVIEW_COL_TEXT = 'Awaiting Author Approval'
FORMATTING_COL_TEXT = 'Formatting'
PUBLISHED_COL_TEXT = 'Published'

REFEREE_REJECT_EP = f'{stt_ep}/{REFEREE_REJECTED}/'
UNDER_REFEREE_EP = f'{stt_ep}/{UNDER_REFEREE}/'
AUTHOR_REVISION_EP = f'{stt_ep}/{AUTHOR_REVISION}/'
COPY_EDITING_EP = f'{stt_ep}/{COPY_EDITING}/'
AUTHOR_REVIEW_EP = f'{stt_ep}/{AUTHOR_REVIEW}/'
FORMATTING_EP = f'{stt_ep}/{FORMATTING}/'
PUBLISHED_EP = f'{stt_ep}/{PUBLISHED}/'

COLUMN_OPTIONS_MAP = {
    SUBMITTED: {
        TEXT: SUBMITTED_COL_TEXT,
        OPTIONS: {
            'Suitable': UNDER_REFEREE_EP,
            'Desk Reject': REFEREE_REJECT_EP,
        }
    },
    UNDER_REFEREE: {
        TEXT: UNDER_REFEREE_COL_TEXT,
        OPTIONS: {
            'Accept With Revisions': AUTHOR_REVISION_EP,
            'Accept Without Revisions': COPY_EDITING_EP,
            'Reject': REFEREE_REJECT_EP,
        }
    },
    AUTHOR_REVISION: {
        TEXT: AUTHOR_REVISION_COL_TEXT,
        OPTIONS: {
            'Accept Revisions': COPY_EDITING_EP,
        }
    },
    COPY_EDITING: {
        TEXT: COPY_EDITING_COL_TEXT,
        OPTIONS: {
            'Complete Copy Editing': AUTHOR_REVIEW_EP,
        }
    },
    AUTHOR_REVIEW: {
        TEXT: AUTHOR_REVIEW_COL_TEXT,
        OPTIONS: {
            'Complete Author Approval': FORMATTING_EP,
        }
    },
    FORMATTING: {
        TEXT: FORMATTING_COL_TEXT,
        OPTIONS: {
            'Complete Formatting': PUBLISHED_EP,
        }
    },
    PUBLISHED: {
        TEXT: PUBLISHED_COL_TEXT,
        OPTIONS: {

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
