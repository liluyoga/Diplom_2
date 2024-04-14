import pytest
import requests
import json
import random
from data import AdditionalVariables, UserData


@pytest.fixture(scope='function')
def generate_new_user_data():
    user_data = UserData.generate_new_user_data()

    yield user_data

    # авторизация и удаление созданного пользователя
    payload = {
        "email": user_data.get("email"),
        "password": user_data.get("password")
    }

    response = requests.post(f'{AdditionalVariables.URL}/api/auth/login', headers={"Content-type": "application/json"}, data=json.dumps(payload))
    token = response.json()["accessToken"]
    requests.delete(f'{AdditionalVariables.URL}/api/auth/user', headers={"Authorization": f'{token}'})


@pytest.fixture(scope='function')
def generate_and_register_new_user():
    user_data = UserData.generate_new_user_data()
    response = requests.post(f'{AdditionalVariables.URL}/api/auth/register', headers={"Content-type": "application/json"}, data=json.dumps(user_data))
    token = response.json()["accessToken"]

    yield user_data, token

    # удаление зарегистрированного пользователя
    requests.delete(f'{AdditionalVariables.URL}/api/auth/user', headers={"Authorization": f'{token}'})


@pytest.fixture(scope='function')
def generate_and_register_two_new_users():
    user_data = [UserData.generate_new_user_data(), UserData.generate_new_user_data()]

    response_0 = requests.post(f'{AdditionalVariables.URL}/api/auth/register',
                             headers={"Content-type": "application/json"}, data=json.dumps(user_data[0]))
    response_1 = requests.post(f'{AdditionalVariables.URL}/api/auth/register', headers={"Content-type": "application/json"}, data=json.dumps(user_data[1]))

    tokens = [response_0.json()["accessToken"], response_1.json()["accessToken"]]

    yield user_data[0], user_data[1], tokens[0]

    # удаление зарегистрированных пользователей
    requests.delete(f'{AdditionalVariables.URL}/api/auth/user', headers={"Authorization": f'{tokens[0]}'})
    requests.delete(f'{AdditionalVariables.URL}/api/auth/user', headers={"Authorization": f'{tokens[1]}'})


@pytest.fixture(scope='function')
def choice_ingredients_for_burger():
    all_ingredients = []
    ingredients_for_burger = []

    response = requests.get(f'{AdditionalVariables.URL}/api/ingredients')

    for item in response.json()["data"]:
        ingredient = item.get("_id")
        all_ingredients.append(ingredient)

    ingredients_for_burger.append(random.choice(all_ingredients))
    ingredients_for_burger.append(random.choice(all_ingredients))
    ingredients_for_burger.append(random.choice(all_ingredients))

    yield ingredients_for_burger


@pytest.fixture(scope='function')
def create_user_and_order(generate_and_register_new_user, choice_ingredients_for_burger):
    token = generate_and_register_new_user[1]
    payload = {
        "ingredients": choice_ingredients_for_burger
    }
    requests.post(f'{AdditionalVariables.URL}/api/orders', headers={"Content-type": "application/json", "Authorization": f'{token}'}, data=json.dumps(payload))

    yield token

    # удаление зарегистрированного пользователя
    requests.delete(f'{AdditionalVariables.URL}/api/auth/user', headers={"Authorization": f'{token}'})
