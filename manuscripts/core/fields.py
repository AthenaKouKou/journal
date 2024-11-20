from backendcore.data.form_filler import (
    DISP_NAME
)
import backendcore.data.fields as cflds
from backendcore.common.constants import OBJ_ID_NM

NAME = cflds.NAME
CODE = cflds.CODE
FLD_TYPE = cflds.FLD_TYPE
MARKDOWN = cflds.MARKDOWN

ABSTRACT = 'abstract'
ABSTRACT_DISP_NAME = 'Abstract'
AUTHORS = 'authors'
AUTHORS_DISP_NAME = 'Authors'
EMAIL = 'contact_email'
EMAIL_DISP_NAME = 'Contact Email'
FILENAME = 'file_name'
HISTORY = 'history'
HISTORY_DISP_NAME = 'Manuscript history'
LAST_UPDATED = 'timeUpdated'
LAST_UPDATED_DISP_NAME = 'Time last updated'
REFEREES = 'referees'
REFEREES_DISP_NAME = 'Referees'
REF_REPORT = 'report'
REF_VERDICT = 'verdict'
STATE = 'state'
STATE_DISP_NAME = 'State'
TEXT = 'text'
TEXT_DISP_NAME = 'Manuscript text'
TEST_FLD_DISP_NM = 'Sample Code'
TEST_FLD_NM = OBJ_ID_NM
TITLE = 'title'
TITLE_DISP_NAME = 'Title'
VERDICT = 'verdict'
WCOUNT = 'wcount'
WCOUNT_DISP_NAME = 'Word Count'

FIELDS = {
    OBJ_ID_NM: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
    TITLE: {
        DISP_NAME: TITLE_DISP_NAME,
    },
    WCOUNT: {
        DISP_NAME: WCOUNT_DISP_NAME,
        FLD_TYPE: cflds.INT,
    },
    AUTHORS: {
        DISP_NAME: AUTHORS_DISP_NAME,
    },
    TEXT: {
        DISP_NAME: TEXT_DISP_NAME,
        cflds.HIDDEN: True,
    },
    ABSTRACT: {
        DISP_NAME: ABSTRACT_DISP_NAME,
        MARKDOWN: 1,
    },
    STATE: {
        DISP_NAME: STATE_DISP_NAME,
    },
    HISTORY: {
        DISP_NAME: HISTORY_DISP_NAME,
        cflds.HIDDEN: True,
    },
    REFEREES: {
        DISP_NAME: REFEREES_DISP_NAME,
        cflds.HIDDEN: True,
        FLD_TYPE: cflds.DICT,
    },
    LAST_UPDATED: {
        DISP_NAME: LAST_UPDATED_DISP_NAME,
    },
}


def get_flds() -> dict:
    return FIELDS


def get_fld_names() -> list:
    return cflds.get_fld_names(FIELDS)


def get_disp_name(fld_nm: str) -> dict:
    return cflds.get_disp_name(FIELDS, fld_nm)


def main():
    print(f'{get_flds()=}')


if __name__ == '__main__':
    main()
