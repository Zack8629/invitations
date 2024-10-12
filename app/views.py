from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from wtforms import SelectField
from wtforms.fields.simple import StringField, URLField

from app.models import db, User, Event, GuestType, SalutationType, ShortLink, QRCode, Role, EventType
from app.services import crypto, link_shortener, generate_qr


class RoleModelView(ModelView):
    pass


class UserModelView(ModelView):
    column_exclude_list = ['password_hash']
    form_extra_fields = {
        'role_id': SelectField('Роль', coerce=int),
        'password_hash': StringField('Пароль'),
    }

    def create_form(self, obj=None):
        form = super(UserModelView, self).create_form(obj)
        form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]

        return form

    def edit_form(self, obj=None):
        form = super(UserModelView, self).edit_form(obj)
        form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]

        delattr(form, 'password_hash')

        return form


class EventTypeModelView(ModelView):
    pass


class EventModelView(ModelView):
    form_extra_fields = {
        'user_id': SelectField('Creator', coerce=int),
        'event_type_id': SelectField('Тип мероприятия', coerce=int),
        'hash_id': StringField('Hash id', render_kw={'readonly': True}),
    }

    def create_form(self, obj=None):
        form = super(EventModelView, self).create_form(obj)
        form.user_id.choices = [
            (user.id,
             f'{user.name}' if user.surname is None else f'{user.name} {user.surname}')
            for user in User.query.all()
        ]
        form.event_type_id.choices = [(event_type.id, event_type.name) for event_type in EventType.query.all()]

        return form

    def edit_form(self, obj=None):
        form = super(EventModelView, self).edit_form(obj)
        form.user_id.choices = [
            (user.id,
             f'{user.name}' if user.surname is None else f'{user.name} {user.surname}')
            for user in User.query.all()
        ]
        form.hash_id.render_kw = {'readonly': True}

        return form

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.hash_id = crypto.encrypt_data(model.id)


class GuestTypeModelView(ModelView):
    pass


class SalutationTypeModelView(ModelView):
    pass


class GuestModelView(ModelView):
    form_extra_fields = {
        'event_id': SelectField('Мероприятие', coerce=int),
        'user_id': SelectField('Создатель мероприятия', coerce=int),
        'guest_type_id': SelectField('Тип гостя', coerce=int),
        'salutation_type_id': SelectField('Salutation Type'),
        'hash_id': StringField('Hash id', render_kw={'readonly': True}),
        'short_url': URLField('Short URL', render_kw={'readonly': True}),
    }

    def create_form(self, obj=None):
        form = super(GuestModelView, self).create_form(obj)
        form.event_id.choices = [(event.id, event.name) for event in Event.query.all()]
        form.salutation_type_id.choices = [
            (salutation.id, salutation.name) for salutation in SalutationType.query.all()
        ]
        form.user_id.choices = [
            (user.id,
             f'{user.name}' if user.surname is None else f'{user.name} {user.surname}')
            for user in User.query.all()
        ]
        form.guest_type_id.choices = [(type_guest.id, type_guest.name) for type_guest in GuestType.query.all()]

        return form

    def on_model_change(self, form, model, is_created):
        if is_created:
            event_id = form.event_id.data

            with db.session.no_autoflush:
                hash_event = Event.query.get(event_id).hash_id

            hash_guest = crypto.encrypt_data(model.id)

            model.hash_id = hash_guest

            original_url = link_shortener.generate_orig_url(hash_event, hash_guest)
            short_url = link_shortener.generate_short_url(original_url)

            short_link_obj = ShortLink(
                short_url=short_url,
                original_url=original_url,
                event_id=event_id,
                guest_id=model.id,
            )

            svg_data = generate_qr.gen_text(short_url)
            qr_obj = QRCode(svg_data=svg_data, event_id=event_id, guest_id=model.id)

            db.session.add(short_link_obj)
            db.session.add(qr_obj)

    def edit_form(self, obj=None):
        form = super(GuestModelView, self).edit_form(obj)
        form.event_id.choices = [(event.id, event.event_name) for event in Event.query.all()]
        form.user_id.choices = [
            (user.id,
             f'{user.name}' if user.surname is None else f'{user.name} {user.surname}')
            for user in User.query.all()
        ]
        form.salutation_type_id.choices = [
            (salutation.id, salutation.name) for salutation in SalutationType.query.all()
        ]
        form.guest_type_id.choices = [(type_guest.id, type_guest.name) for type_guest in GuestType.query.all()]
        form.short_url.data = obj.short_link.short_url

        return form


class PlusOneModelView(ModelView):
    pass


class ChildModelView(ModelView):
    pass


class CommentModelView(ModelView):
    pass


class ResponseOptionModelView(ModelView):
    pass


class ResponseModelView(ModelView):
    pass


class ShortLinkModelView(ModelView):
    form_extra_fields = {
        'short_url': StringField('Short Url', render_kw={'readonly': True}),
        'original_url': StringField('Original Url', render_kw={'readonly': True}),
    }


class QRCodeModelView(ModelView):
    @staticmethod
    def _svg_to_image(self, context, model, name):
        if model.svg_data:
            return Markup(
                f'<img src="data:image/svg+xml;base64,{model.svg_data}" style="max-width: 150px;">'
            )
        else:
            return ''

    column_list = ('guest', 'svg_data')
    column_formatters = {
        'guest': lambda v, c, m, p: m.guest.name,
        'svg_data': _svg_to_image,
    }

    form_extra_fields = {
        'guest': StringField('Guest', render_kw={'readonly': True}),
        'svg_data': StringField('SVG Data', render_kw={'readonly': True}),
    }
