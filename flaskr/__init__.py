from flask import Flask, render_template
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_envvar('YOURAPPLICATION_SETTINGS')
    from . import auth
    app.register_blueprint(auth.bp)
    print(f'app.config {app.config}')

    @app.route('/')
    def hello():
        return render_template('app.html')

    return app