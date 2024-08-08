"""
This module provides a sample query form.
"""

import backendcore.data.form_filler as ff

from manuscripts.fields import (
    ABSTRACT,
    ABSTRACT_DISP_NAME,
    AUTHORS,
    AUTHORS_DISP_NAME,
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
        ff.INPUT_TYPE: ff.LIST,
    },
    {
        ff.FLD_NM: TEXT,
        ff.QSTN: TEXT_DISP_NAME,
        ff.INPUT_TYPE: ff.MARKDOWN,
        ff.OPT: True,
        ff.DISP_ON: ENTRY,
        ff.FLD_LEN: 255,
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
