import os

from flask_admin import Admin as AdminFlask
from flask_admin.menu import MenuLink

from .models import (
    db, Role, User, Event, GuestType, SalutationType, Guest, PlusOne, Child, Comment, ResponseOption, Response,
    ShortLink, QRCode,
)
from .views import (
    RoleModelView, UserModelView, EventModelView, GuestTypeModelView, SalutationTypeModelView, GuestModelView,
    PlusOneModelView, ChildModelView, CommentModelView, ResponseOptionModelView, ResponseModelView, ShortLinkModelView,
    QRCodeModelView
)


def create_app(flask):
    conf_path = os.path.abspath('config.py')
    flask.config.from_pyfile(conf_path)

    try:
        with flask.app_context():
            db.init_app(flask)
            db.create_all()

            admin = AdminFlask(flask, name='Админка пригласительных', template_mode='bootstrap3')
            admin.add_link(MenuLink(name='GO Index!', url='/'))
            admin.add_link(MenuLink(name='404', url='/404'))

            admin.add_view(RoleModelView(Role, db.session, name='Роли'))
            admin.add_view(UserModelView(User, db.session, name='Пользователи'))

            admin.add_view(EventModelView(Event, db.session, name='Мероприятия'))

            admin.add_view(GuestTypeModelView(GuestType, db.session, name='Типы гостей'))
            admin.add_view(SalutationTypeModelView(SalutationType, db.session, name='Типы приветствия'))

            admin.add_view(GuestModelView(Guest, db.session, name='Гости'))
            admin.add_view(PlusOneModelView(PlusOne, db.session, name='Плюс один'))
            admin.add_view(ChildModelView(Child, db.session, name='Дети'))
            admin.add_view(CommentModelView(Comment, db.session, name='Комментарии'))

            admin.add_view(ResponseOptionModelView(ResponseOption, db.session, name='Варианты ответов'))
            admin.add_view(ResponseModelView(Response, db.session, name='Ответы'))

            admin.add_view(ShortLinkModelView(ShortLink, db.session, name='Короткие ссылки'))
            admin.add_view(QRCodeModelView(QRCode, db.session, name='QR Code'))

    except ValueError as V_err:
        print(f'Error initializing database: {V_err}')

    except Exception as err:
        print(f'Error database: {err}')

    return flask
