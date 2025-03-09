import pytest
from fastapi import status

class TestEndpoints:
    @pytest.mark.parametrize(
        'path, expected',
        [
            ('/rooms', status.HTTP_200_OK),
        ]
    )
    def test_get_rooms(self, http_client, path, expected):
        response = http_client.get(path)
        assert response.status_code == expected

    @pytest.mark.parametrize(
        'data, expected_status, expected_detail',
        [
            ('/rooms/1', status.HTTP_200_OK, None),
            ('/rooms/999', status.HTTP_404_NOT_FOUND, "Room not found"),
        ]
    )
    def test_get_room_id(self, http_client, data, expected_status, expected_detail):
        response = http_client.get(data)
        assert response.status_code == expected_status

        json_response = response.json()
        if expected_status == 404:
            assert json_response["detail"] == expected_detail
        else:
            assert "id" in json_response
            assert "name" in json_response
