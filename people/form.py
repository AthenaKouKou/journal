"""
This module provides the journal query form.
"""

import backendcore.data.form_filler as ff

from journal.people.fields import NAME
import journal.people.roles as rls

FORM_FLDS = [
    {
        ff.FLD_NM: NAME,
        ff.QSTN: 'Name:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
    {
        ff.FLD_NM: rls.ROLES,
        ff.QSTN: 'Roles:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.CHOICES: rls.get_choices(),
        ff.MULTI: False,
        ff.OPT: True,
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
