import manuscripts.core.dashboard as mdsh


def test_get_valid_roles():
    assert isinstance(mdsh.get_valid_columns(), list)


def test_is_valid():
    assert mdsh.is_valid(mdsh.TEST_COLUMN)


def test_is_not_valid():
    assert not mdsh.is_valid('Invalid state')


def test_options():
    assert isinstance(mdsh.get_choices()[mdsh.TEST_COLUMN], dict)


def test_get_choices():
    assert isinstance(mdsh.get_choices(), dict)


def test_get_choices_order():
    assert isinstance(mdsh.get_choices_order(), list)
