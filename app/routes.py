from flask import Flask, render_template, redirect

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
