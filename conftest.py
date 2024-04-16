import pytest
import requests
import json
import random
from data import AdditionalVariables
from helper import UserData


@pytest.fixture(scope='function')
def generate_new_user_data():
    user_data = UserData.generate_new_user_data()

    yield user_data

    # авторизация и удаление созданного пользователя
    payload = {
        "email": user_data.get("email"),
        "password": user_data.get("password")
    }

    response = requests.post(AdditionalVariables.URL_API_LOGIN, headers={"Content-type": "application/json"}, data=json.dumps(payload))
    token = response.json()["accessToken"]
    requests.delete(AdditionalVariables.URL_API_USER, headers={"Authorization": f'{token}'})


@pytest.fixture(scope='function')
def generate_and_register_new_user():
    user_data = UserData.generate_new_user_data()
    response = requests.post(AdditionalVariables.URL_API_REGISTER, headers={"Content-type": "application/json"}, data=json.dumps(user_data))
    token = response.json()["accessToken"]

    yield user_data, token

    # удаление зарегистрированного пользователя
    requests.delete(AdditionalVariables.URL_API_USER, headers={"Authorization": f'{token}'})


@pytest.fixture(scope='function')
def choice_ingredients_for_burger():
    all_ingredients = []
    ingredients_for_burger = []

    response = requests.get(AdditionalVariables.URL_API_INGREDIENTS)

    for item in response.json()["data"]:
        ingredient = item.get("_id")
        all_ingredients.append(ingredient)

    ingredients_for_burger.append(random.choice(all_ingredients))
    ingredients_for_burger.append(random.choice(all_ingredients))
    ingredients_for_burger.append(random.choice(all_ingredients))

    return ingredients_for_burger


@pytest.fixture(scope='function')
def create_user_and_order(generate_and_register_new_user, choice_ingredients_for_burger):
    token = generate_and_register_new_user[1]
    payload = {
        "ingredients": choice_ingredients_for_burger
    }
    requests.post(AdditionalVariables.URL_API_ORDERS, headers={"Content-type": "application/json", "Authorization": f'{token}'}, data=json.dumps(payload))

    # возвращаем токен нового пользователя с заказом для теста
    return token
