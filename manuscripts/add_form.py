"""
This module provides a sample query form.
"""

import backendcore.data.form_filler as ff

from manuscripts.fields import (
    ABSTRACT,
    ABSTRACT_DISP_NAME,
    AUTHORS,
    AUTHORS_DISP_NAME,
    EMAIL,
    EMAIL_DISP_NAME,
    TEXT,
    TEXT_DISP_NAME,
    TITLE,
    TITLE_DISP_NAME,
    WCOUNT,
    WCOUNT_DISP_NAME,
)

NOT_IMPLEMENTED = 'This option has not been implemented, check back later.'

FILE = 'FILE'
ENTRY = 'ENTRY'
TEXT_ENTRY = 'textentry'
TEXT_ENTRY_DISP_NAME = 'Paste your text here:'
TEXT_FILE = 'fileentry'
TEXT_FILE_DISP_NAME = 'Upload your manuscript'

FORM_FLDS = [
    {
        ff.FLD_NM: TITLE,
        ff.QSTN: TITLE_DISP_NAME,
        ff.INPUT_TYPE: ff.QUERY_STR,
        'full_width': True,
    },
    {
        ff.FLD_NM: WCOUNT,
        ff.QSTN: WCOUNT_DISP_NAME,
        ff.INPUT_TYPE: ff.NUMERIC,
    },
    {
        ff.FLD_NM: AUTHORS,
        ff.QSTN: AUTHORS_DISP_NAME,
        ff.INPUT_TYPE: ff.OBJ_LIST,
        ff.SUBFIELDS: [
            {
                ff.FLD_NM: 'name',
                ff.QSTN: 'Author name',
            },
            {
                ff.FLD_NM: 'email',
                ff.QSTN: 'Author email address',
            },
        ]
    },
    {
        ff.FLD_NM: EMAIL,
        ff.QSTN: EMAIL_DISP_NAME,
        ff.INPUT_TYPE: ff.QUERY_STR,
    },
    {
        ff.FLD_NM: TEXT,
        ff.QSTN: TEXT_DISP_NAME,
        ff.CHOICES: {
            FILE: 'File upload (docx)',
            ENTRY: 'Direct text entry',
        },
        ff.OPT: False,
        ff.DEFAULT: ENTRY,
        ff.MULTI: False,
        ff.SUBFIELDS: [
            {
                ff.FLD_NM: TEXT_ENTRY,
                ff.QSTN: TEXT_ENTRY_DISP_NAME,
                ff.INPUT_TYPE: ff.MARKDOWN,
                ff.OPT: True,
                ff.DISP_ON: ENTRY,
                ff.FLD_LEN: 255,
            },
            {
                ff.FLD_NM: TEXT_FILE,
                ff.QSTN: TEXT_FILE_DISP_NAME,
                ff.INPUT_TYPE: ff.FILE_LOADER,
                ff.OPT: True,
                ff.DISP_ON: FILE,
                ff.FULL_WIDTH: True,
                ff.FILE_TYPES: [ff.DOCX, ff.HTML, ff.TXT, ff.MD]
            },
        ]
    },
    {
        ff.FLD_NM: ABSTRACT,
        ff.QSTN: ABSTRACT_DISP_NAME,
        ff.INPUT_TYPE: ff.MARKDOWN,
        ff.FLD_LEN: 255,
    },
]


def get_form() -> list:
    return FORM_FLDS


def get_form_descr():
    """
    For Swagger!
    """
    return ff.get_form_descr(FORM_FLDS)


def get_fld_names() -> list:
    return ff.get_fld_names(FORM_FLDS)


def main():
    print(f'Form: {get_form()=}')
    print(f'Form: {get_form_descr()=}')
    print(f'Field names: {get_fld_names()=}')


if __name__ == "__main__":
    main()
