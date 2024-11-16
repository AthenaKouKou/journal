from backendcore.data.form_filler import (
    DESCR,
    DISP_NAME,
)
import backendcore.data.fields as cflds
from backendcore.common.constants import EMAIL

VERDICT = 'verdict'
REPORT = 'report'

TEST_FLD_NM = EMAIL
TEST_FLD_DISP_NM = 'Email'


FIELDS = {
    EMAIL: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
    VERDICT: {
        DISP_NAME: 'Verdict',
        DESCR: "The referee's verdict."
    },
    REPORT: {
        DISP_NAME: 'Report',
        DESCR: "The referee's report."
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
