from flask import Flask, render_template, redirect

from app.services import link_shortener

flask_app = Flask(__name__)


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@flask_app.route('/event/guest')
def rsvp():
    return render_template('rsvp.html')


@flask_app.route('/<short_url>')
def redirect_to_original(short_url):
    original_url = link_shortener.redirect(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return render_template('404.html')
