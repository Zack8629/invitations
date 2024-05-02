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

    def admin_role(self, quantity):
        for i in range(quantity):
            i = i + 1
            data = {
                'role_name': f'Root_{i}'
            }
            post_url = '/admin/adminroles/new/?url=/admin/adminroles/'

            # Отправляем POST-запрос для создания гостя
            response = requests.post(self.base_url + post_url, data=data)
            code = response.status_code

            # Проверяем успешность запроса
            if code == 200 or code == 302:
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

            # Отправляем POST-запрос для создания гостя
            response = requests.post(self.base_url + post_url, data=data)
            code = response.status_code

            # Проверяем успешность запроса
            if code == 200 or code == 302:
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

            # Отправляем POST-запрос для создания гостя
            response = requests.post(self.base_url + post_url, data=data)
            code = response.status_code

            # Проверяем успешность запроса
            if code == 200 or code == 302:
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

            # Отправляем POST-запрос для создания гостя
            response = requests.post(self.base_url + post_url, data=data)
            code = response.status_code

            # Проверяем успешность запроса
            if code == 200 or code == 302:
                print(f'Мероприятие: "{data['event_name']}" успешно создано! Код ответа:{code}')
            else:
                print(f'Ошибка при создании мероприятия: "{data['event_name']}"! Код ответа:{code}')

    def create_guest_type(self, quantity):
        for i in range(quantity):
            i = i + 1
            data = {
                'name': f'Тип_гостя_{i}',
            }
            post_url = '/admin/guesttype/new/?url=/admin/guesttype/'

            # Отправляем POST-запрос для создания гостя
            response = requests.post(self.base_url + post_url, data=data)
            code = response.status_code

            # Проверяем успешность запроса
            if code == 200 or code == 302:
                print(f'Тип гостя: "{data['name']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании типа гостя: "{data['name']}"! Код ответа:{code}')

    def create_salutation_type(self, quantity):
        for i in range(quantity):
            i = i + 1
            data = {
                'salutation': f'Ты_{i}',
            }
            post_url = '/admin/salutationtype/new/?url=/admin/salutationtype/'

            # Отправляем POST-запрос для создания гостя
            response = requests.post(self.base_url + post_url, data=data)
            code = response.status_code

            # Проверяем успешность запроса
            if code == 200 or code == 302:
                print(f'Тип приветствия: "{data['salutation']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании типа приветствия: "{data['salutation']}"! Код ответа:{code}')

    def create_guest(self, quantity):
        for i in range(quantity):
            i = i + 1
            data = {
                'name_1': f'Гость_{i}',
                'event_id': 1,
                'creator_id': 1,
                'guest_type': 1,
                # 'surname_1': None,
                # 'name_2': None,
                # 'surname_2': None,
                'salutation_type_id': 1,
                # 'hash_id': None,
                # 'additional_details': None,
                # 'ask_plus_one': False,
                # 'ask_children': False,
                # 'children_count': 0,
                # 'make_paper_invitation': False,
                # 'short_link': '159',
            }
            post_url = '/admin/guest/new/?url=/admin/guest/'

            # Отправляем POST-запрос для создания гостя
            response = requests.post(self.base_url + post_url, data=data)
            code = response.status_code

            # Проверяем успешность запроса
            if code == 200 or code == 302:
                print(f'Гость: "{data['name_1']}" успешно создан! Код ответа:{code}')
            else:
                print(f'Ошибка при создании гостя: "{data['name_1']}"! Код ответа:{code}')

    def create_all_data(self, quantity):
        for i in range(quantity):
            i = i + 1
            print(f'{i} круг создания данных.')
            self.admin_role(i)
            self.create_admins(i)
            self.create_creator(i)
            self.create_event(i)
            self.create_guest_type(i)
            self.create_salutation_type(i)
            self.create_guest(i + 12)
            print()


if __name__ == '__main__':
    create = CreateAppData(BASE_URL)
    dell = False

    if dell:
        create.dell_all_db(app, db, dell)
    else:
        create.create_all_data(1)

    print()
