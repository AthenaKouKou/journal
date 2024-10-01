AU = 'AU'
AUTHOR = 'Author'
CE = 'CE'
CONSULTING_ED = 'Consulting Editor'
CO = 'CO'
COPY_ED = 'Copy Editor'
DE = 'DE'
DEPUTY_ED = 'Deputy Editor'
EB = 'EB'
ED_BOARD = 'Editorial Board'
ED = 'ED'
EDITOR = 'Editor'
JE = 'JE'
JUNIOR_ED = 'Junior Editor'
ME = 'ME'
MAN_ED = 'Managing Editor'
RE = 'RE'
REFEREE = 'Referee'
SE = 'SE'
SENIOR_ADVISOR = 'Senior Advisor'
SP = 'SP'
SPECIAL_ADVISOR = 'Special Advisor Council'

ROLE = 'role'
ROLES = 'roles'

TEST_ROLE = ED

ROLE_MAP = {
    AU: AUTHOR,
    CO: COPY_ED,
    DE: DEPUTY_ED,
    EB: ED_BOARD,
    ED: EDITOR,
    JE: JUNIOR_ED,
    ME: MAN_ED,
    RE: REFEREE,
    SE: SENIOR_ADVISOR,
    SP: SPECIAL_ADVISOR,
}

MASTHEAD_ROLES = [ED, EB, JE, SE, SP]

VALID_ROLES = list(ROLE_MAP.keys())


def get_masthead_roles():
    return MASTHEAD_ROLES


def get_valid_roles() -> list:
    """
    So others can discover what they can use as roles.
    """
    return VALID_ROLES


def is_valid(candidate: str) -> bool:
    """
    Check a candidate role to see if it's valid.
    """
    return candidate in VALID_ROLES


def get_choices():
    return ROLE_MAP


def get_descr(code):
    return ROLE_MAP.get(code)
