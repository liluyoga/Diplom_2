import requests
import json
import pytest
from data import AdditionalVariables
from helper import UserData
import allure


class TestUser:

    @allure.title("Проверка возможности изменить данные пользователя: email/name с авторизацией")
    @pytest.mark.parametrize("key, value",
                             [
                                 ["email", UserData.generate_email()],
                                 ["name", UserData.generate_name()]
                             ]
                             )
    def test_modify_user_data_email_or_name_success(self, generate_and_register_new_user, key, value):
        user_data, token = generate_and_register_new_user
        user_data[key] = value
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        response = requests.patch(AdditionalVariables.URL_API_USER, headers=headers, data=json.dumps(user_data))

        assert response.status_code == 200 and response.json()["user"][key] == user_data[key], (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["user"][key]}'
        )

    @allure.title("Проверка возможности изменить данные пользователя: password с авторизацией")
    def test_modify_user_data_password_success(self, generate_and_register_new_user):
        user_data, token = generate_and_register_new_user
        user_data["password"] = UserData.generate_password()
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        response = requests.patch(AdditionalVariables.URL_API_USER, headers=headers,
                                  data=json.dumps(user_data))

        assert response.status_code == 200 and response.json()["success"] == True, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}'
        )

    @allure.title("Проверка невозможности изменить данные пользователя без авторизации")
    @pytest.mark.parametrize("key, value",
                             [
                                 ["email", UserData.generate_email()],
                                 ["name", UserData.generate_name()],
                                 ["password", UserData.generate_password()]
                             ]
                             )
    def test_modify_user_data_unauthorized(self, generate_and_register_new_user, key, value):
        user_data, _ = generate_and_register_new_user
        user_data[key] = value
        headers = {"Content-type": "application/json", "Authorization": ""}
        response = requests.patch(AdditionalVariables.URL_API_USER, headers=headers,
                                  data=json.dumps(user_data))

        expected_response = {"success": False, "message": AdditionalVariables.ERROR_401_NOT_AUTHORIZED}

        assert response.status_code == 401 and response.json() == expected_response, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )
