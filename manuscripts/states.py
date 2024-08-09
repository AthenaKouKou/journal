"""
This contains manuscript state info
"""

STATE_MAP_EP = 'state_map'


# State (in alphabetical order)
AUTHOR_REVIEW = 'author-review'
COPY_EDITING = 'copy-editing'
EDITOR_REVIEW = 'editor-review'
FORMATTING = 'formatting'
PUBLISHED = 'published'
REFEREE_REVIEW = 'referee-review'
REJECTED = 'rejected'
SUBMITTED = 'submitted'
WITHDRAWN = 'withdrawn'

TEST_STATE = SUBMITTED

# State map
STATE_MAP = {
    AUTHOR_REVIEW: 'Awaiting author review',
    COPY_EDITING: 'The copy editing',
    EDITOR_REVIEW: 'Awaiting editor review',
    FORMATTING: 'Undergoing formatting',
    PUBLISHED: 'Published',
    REFEREE_REVIEW: 'Referees reviewing',
    REJECTED: 'Rejected',
    SUBMITTED: 'Submitted',
    WITHDRAWN: 'Author has withdrawn',
}

VALID_STATES = list(STATE_MAP.keys())


VALID_ACTIONS = []


def get_valid_states() -> list:
    """
    For discovering the names of states.
    """
    return VALID_STATES


def is_valid_state(candidate: str) -> bool:
    """
    For checking if a state is acceptable.
    """
    return candidate in get_valid_states()


def get_valid_actions() -> list:
    """
    For discovering the names of actions.
    """
    return VALID_ACTIONS


def is_valid_action(candidate: str) -> bool:
    """
    For checking if a action is acceptable.
    """
    return candidate in get_valid_actions()


def get_state_choices():
    return STATE_MAP
