from unittest.mock import patch

import journal_api.journal as jrnl

TEST_USER = 'test@test.com'
TEST_AUTH_KEY = 'some_auth_key'


class Request():
    def __init__(self, json: dict):
        self.json = json

    def is_json():
        # DOING THIS BECAUSE WE ARE USING A FAKE REQUEST OBJECR
        # SHOULD FIND A WAY TO TRULY MOCK REQUESTS
        return True


FAKE_REQUEST = Request({jrnl.EDITOR: TEST_USER})


@patch('backendcore.api.common.get_auth_key_from_request',
       autospec=True, return_value=TEST_AUTH_KEY)
def test_get_user_info(mock_auth_key):
    user_id, auth_key = jrnl._get_user_info(FAKE_REQUEST)
    assert user_id == TEST_USER
    assert auth_key == TEST_AUTH_KEY
