import requests
import json
import pytest
from data import AdditionalVariables
from helper import UserData
import allure


class TestRegister:

    @allure.title("Проверка регистрации уникального пользователя")
    def test_registration_unique_user_success(self, generate_new_user_data):
        payload = json.dumps(generate_new_user_data)
        headers = {"Content-type": "application/json"}
        response = requests.post(AdditionalVariables.URL_API_REGISTER, headers=headers, data=payload)

        assert response.status_code == 200 and response.json()["success"] == True, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}'
        )

    @allure.title("Проверка невозможности регистрации пользователя, который уже зарегистрирован")
    def test_registration_same_user_forbidden(self, generate_new_user_data):
        payload = json.dumps(generate_new_user_data)
        headers = {"Content-type": "application/json"}
        requests.post(AdditionalVariables.URL_API_REGISTER, headers=headers, data=payload)
        response = requests.post(AdditionalVariables.URL_API_REGISTER, headers=headers, data=payload)

        expected_response = {"success": False, "message": AdditionalVariables.ERROR_403_USER_ALREADY_EXISTS}

        assert response.status_code == 403 and response.json() == expected_response, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )

    @allure.title("Проверка невозможности регистрации пользователя с незаполненным/отсутствующим обязательным полем")
    @pytest.mark.parametrize("user_data", [
        UserData.generate_new_user_data_empty_email(),
        UserData.generate_new_user_data_empty_password(),
        UserData.generate_new_user_data_empty_name(),
        UserData.generate_new_user_data_without_email(),
        UserData.generate_new_user_data_without_password(),
        UserData.generate_new_user_data_without_name()
    ])
    def test_registration_without_obligatory_field_forbidden(self, user_data):
        payload = json.dumps(user_data)
        headers = {"Content-type": "application/json"}
        response = requests.post(AdditionalVariables.URL_API_REGISTER, headers=headers, data=payload)

        expected_response = {"success": False, "message": AdditionalVariables.ERROR_403_FIELDS_REQUIRED}

        assert response.status_code == 403 and response.json() == expected_response, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )
