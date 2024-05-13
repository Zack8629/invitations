from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class ForeignKeyMixin:
    __abstract__ = True

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)


# Модель роли пользователя
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    users = db.relationship('User', backref='role', lazy=True)


# Модель пользователя
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String)
    phone_number = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    events = db.relationship('Event', backref='created_events', lazy=True, cascade='all, delete-orphan')


# Модель Мероприятия
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    location = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hash_id = db.Column(db.String, unique=True, nullable=False)
    guests = db.relationship('Guest', backref='event', lazy=True, cascade='all, delete-orphan')


# Модель типов гостей
class GuestType(db.Model):
    __tablename__ = 'guest_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


# Модель типов приветствия гостей
class SalutationType(db.Model):
    __tablename__ = 'salutation_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


# Модель Гостя
class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    guest_type_id = db.Column(db.Integer, db.ForeignKey('guest_types.id'), nullable=False)
    salutation_type_id = db.Column(db.Integer, db.ForeignKey('salutation_types.id'), nullable=False)

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


# Модель +1 гостя
class PlusOne(db.Model, ForeignKeyMixin):
    __tablename__ = 'plus_one'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String)
    details = db.Column(db.String)


# Модель Ребёнка
class Child(db.Model, ForeignKeyMixin):
    __tablename__ = 'children'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    details = db.Column(db.String)


# Модель Комментария
class Comment(db.Model, ForeignKeyMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


# Модель Вариантов ответа
class ResponseOption(db.Model):
    __tablename__ = 'response_options'

    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String, nullable=False)


# Модель для Ответа на приглашение
class Response(db.Model, ForeignKeyMixin):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    response_option_id = db.Column(db.Integer, db.ForeignKey('response_options.id'), nullable=False)


# Модель Короткой ссылки
class ShortLink(db.Model, ForeignKeyMixin):
    __tablename__ = 'short_links'

    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String, nullable=False, unique=True)
    original_url = db.Column(db.String, nullable=False, unique=True)
    guest = db.relationship('Guest', back_populates='short_link')


# Модель QR-кода
class QRCode(db.Model, ForeignKeyMixin):
    __tablename__ = 'qr_codes'

    id = db.Column(db.Integer, primary_key=True)
    svg_data = db.Column(db.Text, nullable=False)
    guest = db.relationship('Guest', back_populates='qr_code')


@db.event.listens_for(User, 'before_insert')
def create_password_hash(mapper, connection, target):
    target.password_hash = generate_password_hash(target.password_hash)


def check_password(obj, password):
    try:
        return check_password_hash(obj.password_hash, password)

    except ValueError:
        return False

    except Exception:
        print(f'check_password Exception => {Exception}')
        return False


# Создание индексов и уникальных ограничений
db.Index('idx_users_email', User.email, unique=True)
db.Index('idx_users_phone_number', User.phone_number, unique=True)
db.Index('idx_events_hash_id', Event.hash_id, unique=True)
db.Index('idx_guests_hash_id', Guest.hash_id, unique=True)
