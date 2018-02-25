import sys

from flask import Flask,request,Response,jsonify,Blueprint

from flask_sqlalchemy import SQLAlchemy
import settings
from api.endpoints.manage import ns as managens


from api.define import api

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

def configure_app(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    api.add_namespace(managens)

    flask_app.register_blueprint(blueprint)
    db.app = flask_app
    db.init_app(flask_app)

initialize_app(app)


def main():

    app.run(debug=settings.FLASK_DEBUG,port=5010)

if __name__ == "__main__":
    main()
