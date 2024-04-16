import requests
import json
from data import AdditionalVariables
import allure


class TestLogin:

    @allure.title("Проверка авторизации под существующим пользователем (корректные логин и пароль)")
    def test_login_existing_user_success(self, generate_and_register_new_user):
        user_data, _ = generate_and_register_new_user
        payload = {
            "email": user_data.get("email"),
            "password": user_data.get("password")
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(AdditionalVariables.URL_API_LOGIN, headers=headers, data=json.dumps(payload))

        assert response.status_code == 200 and response.json()["success"] == True, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}'
        )

    @allure.title("Проверка авторизации с неверным логином email")
    def test_login_with_incorrect_email_unauthorized(self, generate_and_register_new_user):
        user_data, _ = generate_and_register_new_user
        payload = {
            "email": f'1{user_data.get("email")}',
            "password": user_data.get("password")
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(AdditionalVariables.URL_API_LOGIN, headers=headers, data=json.dumps(payload))

        expected_response = {"success": False, "message": AdditionalVariables.ERROR_401_INCORRECT}

        assert response.status_code == 401 and response.json() == expected_response, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )

    @allure.title("Проверка авторизации с неверным паролем password")
    def test_login_with_incorrect_password_unauthorized(self, generate_and_register_new_user):
        user_data, _ = generate_and_register_new_user
        payload = {
            "email": user_data.get("email"),
            "password": f'{user_data.get("password")}1'
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(AdditionalVariables.URL_API_LOGIN, headers=headers, data=json.dumps(payload))

        expected_response = {"success": False, "message": AdditionalVariables.ERROR_401_INCORRECT}

        assert response.status_code == 401 and response.json() == expected_response, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )
