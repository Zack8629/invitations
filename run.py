from app import create_app
from app.routes import flask_app

app = create_app(flask_app)

if __name__ == '__main__':
    app.run()
