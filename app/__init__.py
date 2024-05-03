import os

from flask_admin import Admin as AdminFlask
from flask_admin.menu import MenuLink

from .models import (
    db, AdminRoles, Admins, Creator, Event, GuestType, Guest, PlusOne,
    Child, Comment, Response, ResponseOption, ShortLink, QRCode,
    SalutationType
)
from .views import (
    AdminsModelView, EventModelView, GuestTypeModelView, GuestModelView, AdminRolesModelView,
    CreatorModelView, PlusOneModelView, ChildModelView,
    ConnectionGuestPlusOneChildModelView, CommentModelView, ResponseModelView,
    ResponseOptionModelView, ShortLinkModelView, QRCodeModelView, SalutationTypeModelView
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

            admin.add_view(AdminRolesModelView(AdminRoles, db.session))
            admin.add_view(AdminsModelView(Admins, db.session))

            admin.add_view(CreatorModelView(Creator, db.session))
            admin.add_view(EventModelView(Event, db.session))

            admin.add_view(GuestTypeModelView(GuestType, db.session))
            admin.add_view(SalutationTypeModelView(SalutationType, db.session))
            admin.add_view(ResponseOptionModelView(ResponseOption, db.session))

            admin.add_view(GuestModelView(Guest, db.session))
            admin.add_view(PlusOneModelView(PlusOne, db.session))
            admin.add_view(ChildModelView(Child, db.session))
            admin.add_view(CommentModelView(Comment, db.session))
            admin.add_view(ResponseModelView(Response, db.session))
            admin.add_view(ShortLinkModelView(ShortLink, db.session))
            admin.add_view(QRCodeModelView(QRCode, db.session, name='QR Code'))

    except ValueError as V_err:
        print(f'Error initializing database: {V_err}')

    except Exception as err:
        print(f'Error database: {err}')

    return flask
