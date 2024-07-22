import people.roles as rls


def test_get_masthead_roles():
    assert isinstance(rls.get_masthead_roles(), list)


def test_get_descr():
    assert isinstance(rls.get_descr(rls.TEST_ROLE), str)


def test_get_descr_no_such_role():
    assert rls.get_descr('Not a role') is None


def test_get_valid_roles():
    assert isinstance(rls.get_valid_roles(), list)


def test_is_valid():
    assert rls.is_valid(rls.TEST_ROLE)


def test_is_not_valid():
    assert not rls.is_valid('Not a real role')


def test_get_choices():
    assert isinstance(rls.get_choices(), dict)
