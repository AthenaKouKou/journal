from backendcore.data.form_filler import (
    DESCR,
    DISP_NAME,
    FLD_TYPE,
    LIST,
)
import backendcore.data.fields as cflds

from backendcore.common.constants import (
    EMAIL,
    MAP,
)

import people.roles as rls
from people.roles import ROLES

AFFILIATION = 'affiliation'
BIO = 'bio'
NAME = cflds.NAME
POSITION = 'position'
USER_ID = 'user_id'


TEST_FLD_NAME = NAME
NAME_DISP = 'Name'
TEST_FLD_DISP_NAME = NAME_DISP
SAMPLE_NAME = 'Elen Callahan'

FIELDS = {
    NAME: {
        DISP_NAME: NAME_DISP,
    },
    POSITION: {
        DISP_NAME: 'Position',
    },
    AFFILIATION: {
        DISP_NAME: 'Affiliation',
    },
    ROLES: {
        DISP_NAME: 'Roles',
        DESCR: 'What roles does this person play in the journal?',
        FLD_TYPE: LIST,
        MAP: rls.get_choices(),
    },
    EMAIL: {
        DISP_NAME: 'Email',
    },
    BIO: {
        DISP_NAME: 'Bio',
        cflds.MAX_LEN: 80,
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
