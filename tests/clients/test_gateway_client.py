from unittest.mock import patch


def test_get_user_context(gateway_client, user_claims_context):
    expected_context = "user-context"

    with patch.object(
        gateway_client,
        "_build_user_context",
        return_value=expected_context,
    ) as build_mock:
        result = gateway_client._get_user_context()

    assert result == expected_context
    build_mock.assert_called_once_with(user_claims_context)
