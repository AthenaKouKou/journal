import manuscripts.status as mstt


def test_get_valid_roles():
    assert isinstance(mstt.get_valid_statuses(), list)


def test_is_valid():
    assert mstt.is_valid(mstt.TEST_STATUS)


def test_is_not_valid():
    assert not mstt.is_valid('Invalid status')


def test_get_choices():
    assert isinstance(mstt.get_choices(), dict)
