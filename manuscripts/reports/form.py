"""
This module provides a sample query form.
"""

import backendcore.data.form_filler as ff

from manuscripts.reports.fields import (
    EMAIL,
    REPORT,
    VERDICT,
)

FORM_FLDS = [
    {
        ff.FLD_NM: EMAIL,
        ff.QSTN: "Referee's email:",
    },
    {
        ff.FLD_NM: VERDICT,
        ff.QSTN: "Referee's verdict:",
    },
    {
        ff.FLD_NM: REPORT,
        ff.QSTN: "Referee's report:",
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
