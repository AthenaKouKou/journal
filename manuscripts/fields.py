from backendcore.data.form_filler import (
    DESCR, DISP_NAME
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
HISTORY = 'history'
HISTORY_DISP_NAME = 'Manuscript history'
LAST_UPDATED = 'last_updated'
LAST_UPDATED_DISP_NAME = 'Time last updated'
REFEREES = 'referees'
REFEREES_DISP_NAME = 'Referees'
STATUS = 'status'
STATUS_DISP_NAME = 'Status'
SUBMISSION = 'submission'
SUBMISSION_DISP_NAME = 'Manuscript submission'
TEST_FLD_DISP_NM = 'Sample Code'
TEST_FLD_NM = OBJ_ID_NM
TITLE = 'title'
TITLE_DISP_NAME = 'Title'
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
        DESCR: 'Approximate number of words',
        FLD_TYPE: 'INT',
    },
    AUTHORS: {
        DISP_NAME: AUTHORS_DISP_NAME,
        DESCR: 'List of authors',
    },
    SUBMISSION: {
        DISP_NAME: SUBMISSION_DISP_NAME,
        DESCR: 'Text submission; file upload or text entry',
    },
    ABSTRACT: {
        DISP_NAME: ABSTRACT_DISP_NAME,
        MARKDOWN: 1,
    },
    STATUS: {
        DISP_NAME: STATUS_DISP_NAME,
    },
    HISTORY: {
        DISP_NAME: HISTORY_DISP_NAME,
        cflds.HIDDEN: True,
    },
    REFEREES: {
        DISP_NAME: REFEREES_DISP_NAME,
        DESCR: 'The manuscript\'s currently assigned referees.',
        FLD_TYPE: cflds.LIST,
    },
    LAST_UPDATED: {
        DISP_NAME: LAST_UPDATED_DISP_NAME,
        DESCR: 'The time when the manuscript\'s status was last updated.',
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
