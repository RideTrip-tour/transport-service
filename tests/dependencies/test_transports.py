from unittest.mock import patch

from app.dependencies.transports import get_gateway_client


def test_get_gateway_client(gateway_client):
    with patch(
        "app.dependencies.transports.GatewayClient",
        return_value=gateway_client,
    ) as client_mock:
        result = get_gateway_client()

    client_mock.assert_called_once_with()
    assert result is gateway_client
