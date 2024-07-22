"""
This contains manuscript status info
"""

STATUS_MAP_EP = 'status_map'


# Status (in alphabetical order)
AUTHOR_REVIEW = 'author-review'
AUTHOR_REVISION = 'author-revision'
COPY_EDITING = 'copy-editing'
DESK_REJECTED = 'desk-rejected'
FORMATTING = 'formatting'
PUBLISHED = 'published'
REFEREE_ACCEPTED = 'referee-accepted'
REFEREE_ACCEPT_W_REV = 'referee-accept-with-revisions'
REFEREE_REJECTED = 'referee-rejected'
SUBMITTED = 'submitted'
UNDER_EDITOR = 'with-editor'
UNDER_REFEREE = 'with-referee'

TEST_STATUS = SUBMITTED

# Status map
STATUS_MAP = {
    AUTHOR_REVIEW: 'Awaiting author approval',
    AUTHOR_REVISION: 'Author revising',
    COPY_EDITING: 'The copy editing',
    DESK_REJECTED: 'Desk rejected',
    FORMATTING: 'Undergoing formatting',
    PUBLISHED: 'Published',
    REFEREE_ACCEPTED: 'Accepted by referees',
    REFEREE_ACCEPT_W_REV: 'Needs revisions',
    REFEREE_REJECTED: 'Rejected by referees',
    SUBMITTED: 'Submitted',
    UNDER_EDITOR: 'Journal editor reviewing',
    UNDER_REFEREE: 'Referees reviewing',
}

VALID_STATUSES = list(STATUS_MAP.keys())


def get_valid_statuses() -> list:
    """
    For discovering the names of statuses.
    """
    return VALID_STATUSES


def is_valid(candidate: str) -> bool:
    """
    For checking if a status is acceptable.
    """
    return candidate in VALID_STATUSES


def get_choices():
    return STATUS_MAP
