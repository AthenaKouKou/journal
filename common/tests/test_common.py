from unittest.mock import patch

import common.common as jcmn


@patch('os.getenv', return_value='SFA', autospec=True)
def test_get_journal(mock_env):
    journal = jcmn.get_journal()
    assert isinstance(journal, str)
    assert len(journal) > 0


FOO = 'FOO'


@patch('os.getenv', return_value='SFA', autospec=True)
def test_get_collect_name(mock_env):
    collect_nm = jcmn.get_collect_name(FOO)
    assert FOO in collect_nm
    assert len(collect_nm) > len(FOO)
