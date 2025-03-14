from http.client import responses
import pytest
from fastapi import status
from datetime import datetime, timedelta

from tests.conftest import http_client


class TestEndpoints:
    @pytest.mark.parametrize(
        "path, expected",
        [
            ('/rooms', status.HTTP_200_OK),
            ('/rooms/', status.HTTP_200_OK),
        ]
    )
    def test_get_rooms(self, http_client, path, expected):
        response = http_client.get(path)
        assert response.status_code == expected

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        'path, expected',
        [
            ('/rooms', status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_get_rooms_failed(self, http_client, path, expected):
        response = http_client.get(path)
        assert response.status_code == expected

    @pytest.mark.parametrize(
        'room_id, expected',
        [
            (1, status.HTTP_200_OK),
            (5, status.HTTP_200_OK),
            (999, status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_get_room_by_id_success(self, http_client, room_id, expected):
        response = http_client.get(f'/rooms/{room_id}/')
        assert response.status_code == expected

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        'room_id, expected',
        [
            ('1', status.HTTP_422_UNPROCESSABLE_ENTITY),
        ]
    )
    def test_get_room_by_id_failed(self, http_client, room_id, expected):
        response = http_client.get(f'/rooms/{room_id}/')
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "booking_data, expected_status",
        [
            (
                    {
                        "room_id": 1,
                        "user_id": 1,
                        "check_in": datetime.utcnow().date().isoformat(),
                        "check_out": (datetime.utcnow() + timedelta(days=3)).date().isoformat(),
                        "status": "pending"
                    },
                    status.HTTP_201_CREATED
            ),
        ]
    )
    def test_make_booking(self, http_client, booking_data, expected_status):
        response = http_client.post("/booking/", json=booking_data)
        assert response.status_code == expected_status
        assert response.json()["room_id"] == booking_data["room_id"]
        assert response.json()["user_id"] == booking_data["user_id"]
        assert response.json()["status"] == booking_data["status"]

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "booking_data, expected_status",
        [
            (
                    {
                        "room_id": "invalid",  # noto'g'ri tur
                        "user_id": 1,
                        "check_in": datetime.utcnow().date().isoformat(),
                        "check_out": (datetime.utcnow() + timedelta(days=3)).date().isoformat(),
                        "status": "pending"
                    },
                    status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
        ]
    )
    def test_make_booking_failed(self, http_client, booking_data, expected_status):
        response = http_client.post("/booking/", json=booking_data)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "rooms_path, expected_status",
        [
            ('/rooms_type/', status.HTTP_200_OK),
            ('/rooms_type', status.HTTP_404_NOT_FOUND),
        ]
    )
    def test_get_rooms_type(self, http_client, rooms_path, expected_status):
        response = http_client.get(rooms_path)
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            (
                {
                    "title": "Hello",
                },
                status.HTTP_200_OK,
            )
        ]
    )
    def test_post_rooms_type(self, http_client, payload, expected_status):
        response = http_client.post("/rooms_type/", json=payload)
        assert response.json()["title"] == payload["title"]
        assert response.status_code == expected_status


    @pytest.mark.xfail
    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            (
                    {
                        "title": 3,
                    },
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            (
                    {
                        "title": {},
                    },
                status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        ]
    )
    def test_post_rooms_type_failed(self, http_client, payload, expected_status):
        response = http_client.post("/rooms_type/", json=payload)
        assert response.status_code == expected_status


    @pytest.mark.parametrize(
        "id, data, expected_status",
        [
            (1, "Hello", status.HTTP_200_OK),
            (5, "Hello", status.HTTP_200_OK),
        ]
    )
    def test_get_room_id(self, http_client, id, data, expected_status):
        response = http_client.get(f'/rooms/{id}/')
        assert response.status_code == expected_status
        assert response.json()["id"] == id


    @pytest.mark.parametrize(
        "data_id, expected_status",
        [
            (1, status.HTTP_202_ACCEPTED),
            (5, status.HTTP_202_ACCEPTED),
        ]
    )
    def test_delete_room_id(self, http_client, data_id, expected_status):
        response = http_client.delete(f'/rooms/{data_id}/')
        assert response.status_code == expected_status
