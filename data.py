import random


class AdditionalVariables:

    URL = 'https://stellarburgers.nomoreparties.site'
    ERROR_403_USER_ALREADY_EXISTS = 'User already exists'
    ERROR_403_FIELDS_REQUIRED = 'Email, password and name are required fields'
    ERROR_401_INCORRECT = 'email or password are incorrect'
    ERROR_401_NOT_AUTHORIZED = 'You should be authorised'
    ERROR_403_EMAIL_ALREADY_EXISTS = 'User with such email already exists'
    ERROR_400_NO_INGREDIENT = 'Ingredient ids must be provided'
    INCORRECT_HASH = 'test-hash'


class UserData:

    @staticmethod
    def generate_email():
        email = f'lilu-test{random.randint(0, 999)}@yandex.ru'

        return email

    @staticmethod
    def generate_password():
        password = f'lilu{random.randint(0, 999)}'

        return password

    @staticmethod
    def generate_name():
        name = f'Lilu-{random.randint(0, 999)}'

        return name

    @staticmethod
    def generate_new_user_data():
        user_data = {"email": UserData.generate_email(), "password": UserData.generate_password(), "name": UserData.generate_name()}

        return user_data

    @staticmethod
    def generate_new_user_data_empty_email():
        user_data = {"email": "", "password": UserData.generate_password(), "name": UserData.generate_name()}

        return user_data

    @staticmethod
    def generate_new_user_data_empty_password():
        user_data = {"email": UserData.generate_email(), "password": "", "name": UserData.generate_name()}

        return user_data

    @staticmethod
    def generate_new_user_data_empty_name():
        user_data = {"email": UserData.generate_email(), "password": UserData.generate_password(), "name": ""}

        return user_data

    @staticmethod
    def generate_new_user_data_without_email():
        user_data = {"password": UserData.generate_password(), "name": UserData.generate_name()}

        return user_data

    @staticmethod
    def generate_new_user_data_without_password():
        user_data = {"email": UserData.generate_email(), "name": UserData.generate_name()}

        return user_data

    @staticmethod
    def generate_new_user_data_without_name():
        user_data = {"email": UserData.generate_email(), "password": UserData.generate_password()}

        return user_data
