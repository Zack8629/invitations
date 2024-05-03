from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from wtforms import SelectField
from wtforms.fields.simple import StringField, URLField

from app.models import db, AdminRoles, Creator, Event, GuestType, ShortLink, SalutationType, QRCode
from app.services import crypto, link_shortener, generate_qr


class AdminRolesModelView(ModelView):
    pass


class AdminsModelView(ModelView):
    form_extra_fields = {
        'admin_roles_id': SelectField('Admin Role', coerce=int)
    }

    def create_form(self, obj=None):
        form = super(AdminsModelView, self).create_form(obj)
        form.admin_roles_id.choices = [(role.id, role.role_name) for role in AdminRoles.query.all()]
        return form

    def edit_form(self, obj=None):
        form = super(AdminsModelView, self).edit_form(obj)
        form.admin_roles_id.choices = [(role.id, role.role_name) for role in AdminRoles.query.all()]
        return form


class CreatorModelView(ModelView):
    pass


class EventModelView(ModelView):
    form_extra_fields = {
        'creator_id': SelectField('Creator', coerce=int),
        'hash_id': StringField('Hash id', render_kw={'readonly': True}),
    }

    def create_form(self, obj=None):
        form = super(EventModelView, self).create_form(obj)
        form.creator_id.choices = [
            (creator.id,
             f'{creator.first_name}' if creator.last_name is None else f'{creator.first_name} {creator.last_name}')
            for creator in Creator.query.all()
        ]
        form.hash_id.render_kw = {'readonly': True}

        return form

    def edit_form(self, obj=None):
        form = super(EventModelView, self).edit_form(obj)
        form.creator_id.choices = [
            (creator.id,
             f'{creator.first_name}' if creator.last_name is None else f'{creator.first_name} {creator.last_name}')
            for creator in Creator.query.all()
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
        'event_id': SelectField('Event', coerce=int),
        'creator_id': SelectField('Creator', coerce=int),
        'guest_type': SelectField('Guest Type', coerce=int),
        'hash_id': StringField('Hash id', render_kw={'readonly': True}),
        'short_url': URLField('Short URL', render_kw={'readonly': True}),
        'salutation_type_id': SelectField('Salutation Type'),
        # 'children_count': StringField('Children Count', coerce=int, render_kw={'readonly': True}),
    }

    def create_form(self, obj=None):
        form = super(GuestModelView, self).create_form(obj)
        form.event_id.choices = [(event.id, event.event_name) for event in Event.query.all()]
        form.salutation_type_id.choices = [
            (salutation.id, salutation.salutation) for salutation in SalutationType.query.all()
        ]
        form.creator_id.choices = [
            (creator.id,
             f'{creator.first_name}' if creator.last_name is None else f'{creator.first_name} {creator.last_name}')
            for creator in Creator.query.all()
        ]
        form.guest_type.choices = [(type_guest.id, type_guest.name) for type_guest in GuestType.query.all()]

        return form

    def on_model_change(self, form, model, is_created):
        if is_created:
            db.session.add(model)

            event_id = form.event_id.data

            hash_event = crypto.encrypt_data(event_id)
            hash_guest = crypto.encrypt_data(model.id)

            model.hash_id = hash_guest

            print(f'on_model_change')

            original_url = link_shortener.generate_orig_url(hash_event, hash_guest)
            short_url = link_shortener.generate_short_url(original_url)

            short_link_obj = ShortLink(
                guest_id=model.id, short_url=short_url, original_url=original_url,
            )

            svg_data = generate_qr.gen_text(short_url)
            qr_obj = QRCode(svg_data=svg_data, guest_id=model.id)

            db.session.add(short_link_obj)
            db.session.add(qr_obj)

    def edit_form(self, obj=None):
        form = super(GuestModelView, self).edit_form(obj)
        form.event_id.choices = [(event.id, event.event_name) for event in Event.query.all()]
        form.creator_id.choices = [
            (creator.id,
             f'{creator.first_name}' if creator.last_name is None else f'{creator.first_name} {creator.last_name}')
            for creator in Creator.query.all()
        ]
        form.salutation_type_id.choices = [
            (salutation.id, salutation.salutation) for salutation in SalutationType.query.all()
        ]
        form.guest_type.choices = [(type_guest.id, type_guest.name) for type_guest in GuestType.query.all()]
        form.short_url.data = obj.short_link.short_url

        return form


class PlusOneModelView(ModelView):
    pass


class ChildModelView(ModelView):
    pass


class ConnectionGuestPlusOneChildModelView(ModelView):
    pass


class CommentModelView(ModelView):
    pass


class ResponseModelView(ModelView):
    pass


class ResponseOptionModelView(ModelView):
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
        'svg_data': _svg_to_image,
    }

    form_extra_fields = {
        'guest': StringField('Guest', render_kw={'readonly': True}),
        'svg_data': StringField('SVG Data', render_kw={'readonly': True}),
    }
