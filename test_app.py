import requests

from app import db
from config import BASE_URL
from run import app


class CreateAppData:
    def __init__(self, _base_url):
        self.base_url = _base_url

    @staticmethod
    def dell_all_db(_app, _db, you_are_sure=False):
        print(f'МЕТОД: "dell_all_db" RUN => {you_are_sure}')
        if you_are_sure:
            with _app.app_context():
                _db.drop_all()
                print(f'All db data has been deleted')

    def send_post_request(self, post_url, data):
        response = requests.post(self.base_url + post_url, data=data)
        return response.status_code

    def create_role(self):
        roles = ('Root', 'Admin', 'Пользователь')
        for role in roles:
            data = {
                'name': role
            }
            post_url = '/admin/role/new/?url=/admin/role/'

            code = self.send_post_request(post_url, data)

            if code == 200:
                print(f'Роль: "{data['name']}" успешно создана! Код ответа:{code}')
            else:
                print(f'Ошибка при создании роли: "{data['name']}"! Код ответа:{code}')
        print()

    def create_users(self, quantity):
        if quantity > 0:
            print('Создание Пользователей')

            for i in range(quantity):
                i = i + 1

                if i == 1:
                    role_id = 1
                else:
                    role_id = 3

                data = {
                    'name': f'{i}User',
                    'email': f'{i}User@User.ru',
                    'password_hash': f'User',
                    'role_id': role_id,
                }
                post_url = '/admin/user/new/?url=/admin/user/'

                code = self.send_post_request(post_url, data)

                if code == 200:
                    print(f'Пользователь: "{data['name']}" успешно создан! Код ответа:{code}')
                else:
                    print(f'Ошибка при создании пользователя: "{data['name']}"! Код ответа:{code}')
            print()

    def create_event(self, quantity):
        if quantity > 0:
            print('Создание Мероприятий')

            for i in range(quantity):
                i = i + 1
                data = {
                    'name': f'{i}Мероприятие',
                    'user_id': i,
                }
                post_url = '/admin/event/new/?url=/admin/event/'

                code = self.send_post_request(post_url, data)

                if code == 200:
                    print(f'Мероприятие: "{data['name']}" успешно создано! Код ответа:{code}')
                else:
                    print(f'Ошибка при создании мероприятия: "{data['name']}"! Код ответа:{code}')
            print()

    def create_guest_type(self):
        types_guests = ('Гость', 'Пара', 'Семья')
        for type_guest in types_guests:
            data = {
                'name': type_guest,
            }
            post_url = '/admin/guesttype/new/?url=/admin/guesttype/'

            code = self.send_post_request(post_url, data)

            if code == 200:
                print(f'Тип гостя: "{data['name']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании типа гостя: "{data['name']}"! Код ответа:{code}')
        print()

    def create_salutation_type(self):
        types_salutation = ('Ты', 'Вы', 'Дорогой', 'Дорогая', 'Дорогие')
        for name in types_salutation:
            data = {
                'name': name,
            }
            post_url = '/admin/salutationtype/new/?url=/admin/salutationtype/'

            code = self.send_post_request(post_url, data)

            if code == 200:
                print(f'Тип приветствия: "{data['name']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании типа приветствия: "{data['name']}"! Код ответа:{code}')
        print()

    def create_guest(self, quantity):
        if quantity > 0:
            print('Создание Гостей')

            for i in range(quantity):
                i = i + 1
                data = {
                    'user_id': 1,
                    'event_id': 1,

                    'guest_type_id': 1,
                    'salutation_type_id': 1,

                    'name': f'{i}Гость',
                }
                post_url = '/admin/guest/new/?url=/admin/guest/'

                code = self.send_post_request(post_url, data)

                if code == 200:
                    print(f'Гость: "{data['name']}" успешно создан! Код ответа:{code}')
                else:
                    print(f'Ошибка при создании гостя: "{data['name']}"! Код ответа:{code}')
            print()

    def create_response_option(self):
        options = ('Да', 'Нет')
        for option in options:
            data = {
                'response': f'{option}',
            }
            post_url = '/admin/responseoption/new/?url=/admin/responseoption/'

            code = self.send_post_request(post_url, data)

            if code == 200:
                print(f'Тип ответа: "{data['response']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании типа ответа: "{data['response']}"! Код ответа:{code}')
        print()

    def create_all_data(self, _create_types, _cnt_users, _cnt_events, _cnt_guests):
        try:
            if _create_types:
                print('Создание категорий')
                self.create_role()
                self.create_guest_type()
                self.create_salutation_type()
                self.create_response_option()
                print()

            self.create_users(_cnt_users)
            self.create_event(_cnt_events)
            self.create_guest(_cnt_guests)

        except Exception as err:
            print(f'ОШИБКА => {err=}')


if __name__ == '__main__':
    create = CreateAppData(BASE_URL)

    create_types = True

    cnt_users = 20
    cnt_events = 20
    cnt_guests = 20

    dell = False

    if dell:
        create.dell_all_db(app, db, dell)
    else:
        create.create_all_data(create_types, cnt_users, cnt_events, cnt_guests)
