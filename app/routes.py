from flask import Flask, render_template, redirect, url_for, flash

from app import Admins, Creator
from app.forms import LoginForm
from app.models import check_password
from app.services import link_shortener

flask_app = Flask(__name__)

page_404 = 'base/404.html'


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template(page_404)


@flask_app.route('/<short_url>')
def redirect_to_original(short_url):
    original_url = link_shortener.get_orig_url(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return render_template(page_404)


@flask_app.route('/rsvp')
@flask_app.route('/<event>/<guest>')
def rsvp(event='0', guest='0'):
    print(f'RSVP:')
    print(f'{event=}')
    print(f'{guest=}')
    return render_template('rsvp.html',
                           event=event,
                           guest=guest)


@flask_app.route('/reg')
def reg():
    return render_template('reg.html')


@flask_app.route('/pi')
def pi():
    return render_template('paper_invite.html')


@flask_app.route('/create')
def create():
    return render_template('create.html')


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admins.query.filter_by(email=form.email.data).first()
        creator = Creator.query.filter_by(email=form.email.data).first()

        # Вход в систему как администратор
        if admin is not None and check_password(admin, form.password.data):
            return redirect('/admin')

            # Вход в систему как создатель
        elif creator is not None and check_password(creator, form.password.data):
            print(f'CREATE!')
            return redirect('/create')

        else:
            flash('Неверный Emai или пароль!')

    return render_template('login.html', form=form)
