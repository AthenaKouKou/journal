from backendcore.data.form_filler import (
    DESCR, DISP_NAME
)
import backendcore.data.fields as cflds
from common.constants import OBJ_ID_NM

NAME = cflds.NAME
CODE = cflds.CODE
FLD_TYPE = cflds.FLD_TYPE
MARKDOWN = cflds.MARKDOWN

ABSTRACT = 'abstract'
ABSTRACT_DISP_NAME = 'Abstract'
AUTHORS = 'authors'
AUTHORS_DISP_NAME = 'Authors'
SUBMISSION = 'submission'
SUBMISSION_DISP_NAME = 'Manuscript submission'
TEST_FLD_NM = OBJ_ID_NM
TEST_FLD_DISP_NM = 'Sample Code'
TEXT_FILE = 'textfile'
TEXT_FILE_DISP_NAME = 'Submission text file upload'
TEXT_ENTRY = 'textentry'
TEXT_ENTRY_DISP_NAME = 'Submission text direct entry'
TITLE = 'title'
TITLE_DISP_NAME = 'Title'
WCOUNT = 'wcount'
WCOUNT_DISP_NAME = 'Word Count'
STATUS = 'status'
STATUS_DISP_NAME = 'Status'

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
    # TEXT_FILE: {
    #     DISP_NAME: TEXT_FILE_DISP_NAME,
    # },
    # TEXT_ENTRY: {
    #     DISP_NAME: TEXT_ENTRY_DISP_NAME,
    #     MARKDOWN: 1,
    # },
    ABSTRACT: {
        DISP_NAME: ABSTRACT_DISP_NAME,
        MARKDOWN: 1,
    },
    STATUS: {
        DISP_NAME: STATUS_DISP_NAME,
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
