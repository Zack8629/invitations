from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy()


# Модель для Ролей Администраторов
class AdminRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String, nullable=False)


# Модель для Администраторов
class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin_roles_id = db.Column(db.Integer, db.ForeignKey('admin_roles.id'), nullable=False)


# Модель для Создателя пригласительных
class Creator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    events = db.relationship('Event', backref='event_creator', lazy=True, cascade='all, delete-orphan')


# Модель для Мероприятия
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, nullable=False)
    event_date = db.Column(db.Date)
    event_time = db.Column(db.Time)
    location = db.Column(db.String)
    hash_id = db.Column(db.String, unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'), nullable=False)
    guests = db.relationship('Guest', backref='event', lazy=True, cascade='all, delete-orphan')


# Модель типов гостей
class GuestType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


# Модель типа приветствия
class SalutationType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salutation = db.Column(db.String, unique=True, nullable=False)


# Модель для Варианта ответа
class ResponseOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String, nullable=False)


# Модель для Гостя
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    guest_type = db.Column(db.Integer, db.ForeignKey('guest_type.id'), nullable=False)
    salutation_type_id = db.Column(db.Integer, db.ForeignKey('salutation_type.id'), nullable=False)

    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String)
    details = db.Column(db.String)

    ask_plus_one = db.Column(db.Boolean)
    plus_ones = db.relationship('PlusOne', backref='guest', lazy=True, cascade='all, delete-orphan')

    ask_children = db.Column(db.Boolean)
    children_count = db.Column(db.Integer, default=0)
    children = db.relationship('Child', backref='guest', lazy=True, cascade='all, delete-orphan')

    make_paper_invitation = db.Column(db.Boolean)

    comments = db.relationship('Comment', backref='guest', lazy=True, cascade='all, delete-orphan')
    responses = db.relationship('Response', backref='guest', lazy=True, cascade='all, delete-orphan')

    hash_id = db.Column(db.String, unique=True, nullable=False)
    short_link = db.relationship('ShortLink', uselist=False, back_populates='guest', cascade='all, delete-orphan')
    qr_code = db.relationship('QRCode', uselist=False, back_populates='guest', cascade='all, delete-orphan')


# Модель для +1 гостя
class PlusOne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String)
    details = db.Column(db.String)


# Модель для Ребёнка
class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    details = db.Column(db.String)


# Модель для Комментария
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    text = db.Column(db.Text)


# Модель для Ответа на приглашение
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    response_option_id = db.Column(db.Integer, db.ForeignKey('response_option.id'), nullable=False)


# Модель для Короткой ссылки
class ShortLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    short_url = db.Column(db.String, nullable=False, unique=True)
    original_url = db.Column(db.String, nullable=False, unique=True)
    guest = db.relationship('Guest', back_populates='short_link')


# @event.listens_for(ShortLink, 'before_delete')
# def before_delete_short_link(mapper, connection, target):
#     if target.guest is not None:
#         raise Exception(
#             f'!@#$%! !ShortLink=> {target} невозможно удалить, поскольку она связана с гостем=> {target.guest}!'
#         )


class QRCode(db.Model):
    __tablename__ = 'qr_code'

    id = db.Column(db.Integer, primary_key=True)
    svg_data = db.Column(db.Text, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    guest = db.relationship('Guest', back_populates='qr_code')
