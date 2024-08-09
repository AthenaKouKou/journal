import manuscripts.states as mstt


def test_get_valid_roles():
    assert isinstance(mstt.get_valid_states(), list)


def test_is_valid_state():
    assert mstt.is_valid_state(mstt.TEST_STATE)


def test_is_not_valid_state():
    assert not mstt.is_valid_state('Invalid state')


def test_get_state_choices():
    assert isinstance(mstt.get_state_choices(), dict)
