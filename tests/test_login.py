import requests
import json
from data import AdditionalVariables
import allure


class TestLogin:

    @allure.title("Проверка авторизации под существующим пользователем (корректные логин и пароль)")
    def test_login_existing_user_success(self, generate_and_register_new_user):
        user_data = generate_and_register_new_user[0]
        payload = {
            "email": user_data.get("email"),
            "password": user_data.get("password")
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(f'{AdditionalVariables.URL}/api/auth/login', headers=headers, data=json.dumps(payload))

        assert response.status_code == 200 and response.json()["success"] == True, (
            f'Актуальный результат: {response.status_code}, {response.json()["success"]}'
        )

    @allure.title("Проверка авторизации с неверным логином email")
    def test_login_with_incorrect_email_unauthorized(self, generate_and_register_new_user):
        user_data = generate_and_register_new_user[0]
        payload = {
            "email": f'1{user_data.get("email")}',
            "password": user_data.get("password")
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(f'{AdditionalVariables.URL}/api/auth/login', headers=headers, data=json.dumps(payload))

        assert response.status_code == 401 and response.json()["success"] == False and response.json()["message"] == AdditionalVariables.ERROR_401_INCORRECT, (
            f'Актуальный результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )

    @allure.title("Проверка авторизации с неверным паролем password")
    def test_login_with_incorrect_password_unauthorized(self, generate_and_register_new_user):
        user_data = generate_and_register_new_user[0]
        payload = {
            "email": user_data.get("email"),
            "password": f'{user_data.get("password")}1'
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(f'{AdditionalVariables.URL}/api/auth/login', headers=headers, data=json.dumps(payload))

        assert response.status_code == 401 and response.json()["success"] == False and response.json()["message"] == AdditionalVariables.ERROR_401_INCORRECT, (
            f'Актуальный результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )
