import requests
import json
import pytest
from data import AdditionalVariables, UserData
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
        user_data = generate_and_register_new_user[0]
        token = generate_and_register_new_user[1]
        user_data[key] = value
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        response = requests.patch(f'{AdditionalVariables.URL}/api/auth/user', headers=headers, data=json.dumps(user_data))

        assert response.status_code == 200 and response.json()["success"] == True and response.json()["user"][key] == user_data[key], (
            f'Актуальный результат: {response.status_code}, {response.json()["success"]}, {response.json()["user"][key]}'
        )

    @allure.title("Проверка возможности изменить данные пользователя: password с авторизацией")
    def test_modify_user_data_password_success(self, generate_and_register_new_user):
        user_data = generate_and_register_new_user[0]
        token = generate_and_register_new_user[1]
        user_data["password"] = UserData.generate_password()
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        response = requests.patch(f'{AdditionalVariables.URL}/api/auth/user', headers=headers,
                                  data=json.dumps(user_data))

        assert response.status_code == 200 and response.json()["success"] == True, (
            f'Актуальный результат: {response.status_code}, {response.json()["success"]}'
        )

    @allure.title("Проверка невозможности изменить email на email существующего пользователя")
    def test_modify_user_data_email_existing_forbidden(self, generate_and_register_two_new_users):
        user_data_0 = generate_and_register_two_new_users[0]
        user_data_1 = generate_and_register_two_new_users[1]
        token = generate_and_register_two_new_users[2]
        user_data_0["email"] = user_data_1["email"]
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        response = requests.patch(f'{AdditionalVariables.URL}/api/auth/user', headers=headers,
                                  data=json.dumps(user_data_0))

        assert response.status_code == 403 and response.json()["success"] == False and response.json()[
            "message"] == AdditionalVariables.ERROR_403_EMAIL_ALREADY_EXISTS, (
            f'Актуальный результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
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
        user_data = generate_and_register_new_user[0]
        user_data[key] = value
        headers = {"Content-type": "application/json", "Authorization": ""}
        response = requests.patch(f'{AdditionalVariables.URL}/api/auth/user', headers=headers,
                                  data=json.dumps(user_data))

        assert response.status_code == 401 and response.json()["success"] == False and response.json()["message"] == AdditionalVariables.ERROR_401_NOT_AUTHORIZED, (
            f'Актуальный результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )
