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

    def send_request(self, post_url, data):
        response = requests.post(self.base_url + post_url, data=data)
        return response.status_code

    def admin_role(self):
        roles = ('Root', 'Admin')
        for role in roles:
            data = {
                'role_name': role
            }
            post_url = '/admin/adminroles/new/?url=/admin/adminroles/'

            code = self.send_request(post_url, data)

            if code == 200:
                print(f'Роль админа: "{data['role_name']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании роли админа: "{data['role_name']}"! Код ответа:{code}')

    def create_admins(self, quantity):
        for i in range(quantity):
            i = i + 1
            data = {
                'first_name': f'Root_Admin_{i}',
                'email': f'Root@Admin_{i}.com',
                'password': f'Root_Admin_{i}',
                'admin_roles_id': i,
            }
            post_url = '/admin/admins/new/?url=/admin/admins/'

            code = self.send_request(post_url, data)

            if code == 200:
                print(f'Админ: "{data['first_name']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании админа: "{data['first_name']}"! Код ответа:{code}')

    def create_creator(self, quantity):
        for i in range(quantity):
            i = i + 1
            data = {
                'first_name': f'Создатель_{i}',
                'password': f'Создатель_{i}',
            }
            post_url = '/admin/creator/new/?url=/admin/creator/'

            code = self.send_request(post_url, data)

            if code == 200:
                print(f'Создатель: "{data['first_name']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании создателя: "{data['first_name']}"! Код ответа:{code}')

    def create_event(self, quantity):
        for i in range(quantity):
            i = i + 1
            data = {
                'event_name': f'Мероприятие_{i}',
                'creator_id': i,
            }
            post_url = '/admin/event/new/?url=/admin/event/'

            code = self.send_request(post_url, data)

            if code == 200:
                print(f'Мероприятие: "{data['event_name']}" успешно создано! Код ответа:{code}')
            else:
                print(f'Ошибка при создании мероприятия: "{data['event_name']}"! Код ответа:{code}')

    def create_guest_type(self):
        types_guests = ('Гость', 'Пара', 'Семья')
        for type_guest in types_guests:
            data = {
                'name': type_guest,
            }
            post_url = '/admin/guesttype/new/?url=/admin/guesttype/'

            code = self.send_request(post_url, data)

            if code == 200:
                print(f'Тип гостя: "{data['name']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании типа гостя: "{data['name']}"! Код ответа:{code}')

    def create_salutation_type(self):
        types_salutation = ('Ты', 'Вы', 'Дорогой', 'Дорогая', 'Дорогие')
        for type_salutation in types_salutation:
            data = {
                'salutation': type_salutation,
            }
            post_url = '/admin/salutationtype/new/?url=/admin/salutationtype/'

            code = self.send_request(post_url, data)

            if code == 200:
                print(f'Тип приветствия: "{data['salutation']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании типа приветствия: "{data['salutation']}"! Код ответа:{code}')

    def create_guest(self, quantity):
        for i in range(quantity):
            i = i + 1
            data = {
                'creator_id': 1,
                'event_id': 1,

                'guest_type': 1,
                'salutation_type_id': 1,

                'name': f'Гость_{i}',
            }
            post_url = '/admin/guest/new/?url=/admin/guest/'

            code = self.send_request(post_url, data)

            if code == 200:
                print(f'Гость: "{data['name']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании гостя: "{data['name']}"! Код ответа:{code}')

    def create_response_option(self):
        options = ('Да', 'Нет')
        for option in options:
            data = {
                'response': f'{option}',
            }
            post_url = '/admin/responseoption/new/?url=/admin/responseoption/'

            code = self.send_request(post_url, data)

            if code == 200:
                print(f'Тип ответа: "{data['response']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании типа ответа: "{data['response']}"! Код ответа:{code}')

    def create_all_data(self, quantity):
        try:
            print('Создание категорий')
            self.admin_role()
            self.create_guest_type()
            self.create_salutation_type()
            self.create_response_option()
            print()

            for i in range(quantity):
                i = i + 1
                print(f'{i} круг создания данных.')
                self.create_admins(i)
                self.create_creator(i)
                self.create_event(i)
                self.create_guest(i + 9)
                print()

        except Exception as err:
            print(f'ОШИБКА => {err=}')


if __name__ == '__main__':
    create = CreateAppData(BASE_URL)
    dell = False

    if dell:
        create.dell_all_db(app, db, dell)
    else:
        create.create_all_data(1)
