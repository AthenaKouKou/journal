import manuscripts.reports.fields as flds


def test_is_valid_verdict():
    for verdict in flds.VERDICT_MAP:
        assert flds.is_valid_verdict(verdict)


def test_is_not_valid_verdict():
    assert not flds.is_valid_verdict('surely this is not a ref verdict!')


def test_get_verdict_choices():
    choices = flds.get_verdict_choices()
    assert isinstance(choices, dict)
    assert len(choices) > 1  # If there were only one verdict, why bother?


def test_get_flds():
    assert isinstance(flds.get_flds(), dict)


def test_get_fld_names():
    names = flds.get_fld_names()
    assert isinstance(names, list)
    assert len(names) > 0
    for name in names:
        assert isinstance(name, str)


def test_get_disp_name():
    disp_nm = flds.get_disp_name(flds.TEST_FLD_NM)
    assert disp_nm == flds.TEST_FLD_DISP_NM
