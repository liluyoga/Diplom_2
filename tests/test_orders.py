import json

import allure
import requests

from data import AdditionalVariables


class TestOrders:

    @allure.title("Проверка возможности создания заказа с корректными ингредиентами (с авторизацией)")
    def test_create_order_with_authorization_and_ingredients_success(self, generate_and_register_new_user,
                                                                     choice_ingredients_for_burger):
        _, token = generate_and_register_new_user
        payload = {
            "ingredients": choice_ingredients_for_burger
        }
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        response = requests.post(AdditionalVariables.URL_API_ORDERS, headers=headers, data=json.dumps(payload))

        assert response.status_code == 200 and response.json()["success"] == True, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}'
        )

    @allure.title("Проверка невозможности создания заказа без ингредиентов (с авторизацией)")
    def test_create_order_with_authorization_without_ingredients_badrequest(self, generate_and_register_new_user):
        _, token = generate_and_register_new_user
        payload = {
            "ingredients": []
        }
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        response = requests.post(AdditionalVariables.URL_API_ORDERS, headers=headers, data=json.dumps(payload))

        expected_response = {"success": False, "message": AdditionalVariables.ERROR_400_NO_INGREDIENT}

        assert response.status_code == 400 and response.json() == expected_response, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )

    @allure.title("Проверка передачи невалидного хеша ингредиента")
    def test_create_order_with_authorization_incorrect_hash_ingredients(self, generate_and_register_new_user):
        _, token = generate_and_register_new_user
        payload = {
            "ingredients": [AdditionalVariables.INCORRECT_HASH]
        }
        headers = {"Content-type": "application/json", "Authorization": f'{token}'}
        response = requests.post(AdditionalVariables.URL_API_ORDERS, headers=headers, data=json.dumps(payload))

        assert response.status_code == 500 and 'Internal Server Error' in response.text, (
            f'Фактический результат: {response.status_code}, {response.text}'
        )

    @allure.title("Проверка невозможности создания заказа с корректными ингредиентами, но без авторизации")
    def test_create_order_without_authorization_with_ingredients(self, choice_ingredients_for_burger):
        payload = {
            "ingredients": choice_ingredients_for_burger
        }
        headers = {"Content-type": "application/json", "Authorization": ""}
        response = requests.post(AdditionalVariables.URL_API_ORDERS, headers=headers, data=json.dumps(payload))

        assert response.status_code == 200 and response.json()["success"] == True, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}'
        )

    @allure.title("Проверка невозможности создания заказа без ингредиентов и без авторизации")
    def test_create_order_without_authorization_and_ingredients(self):
        payload = {
            "ingredients": []
        }
        headers = {"Content-type": "application/json", "Authorization": ""}
        response = requests.post(AdditionalVariables.URL_API_ORDERS, headers=headers, data=json.dumps(payload))

        expected_response = {"success": False, "message": AdditionalVariables.ERROR_400_NO_INGREDIENT}

        assert response.status_code == 400 and response.json() == expected_response, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )

    @allure.title("Проверка получения заказов конкретного пользователя с авторизацией")
    def test_get_order_with_authorization_success(self, create_user_and_order):
        token = create_user_and_order
        response = requests.get(AdditionalVariables.URL_API_ORDERS, headers={"Authorization": f'{token}'})

        assert response.status_code == 200 and response.json()["success"] == True, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}'
        )

    @allure.title("Проверка получения заказов без авторизации")
    def test_get_order_without_authorization_unauthorized(self):
        response = requests.get(AdditionalVariables.URL_API_ORDERS, headers={"Authorization": ""})

        expected_response = {"success": False, "message": AdditionalVariables.ERROR_401_NOT_AUTHORIZED}

        assert response.status_code == 401 and response.json() == expected_response, (
            f'Фактический результат: {response.status_code}, {response.json()["success"]}, {response.json()["message"]}'
        )
