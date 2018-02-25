
from flask import Flask,request,Response,jsonify,Blueprint
from database import db
from flask_sqlalchemy import SQLAlchemy
from virgilant_content import settings
from virgilant_content.api.v1.endpoints.data import ns as dataNS
from virgilant_content.api.v1.endpoints.content import ns as contentNS


from virgilant_content.api.define import api


app = Flask(__name__)

def configure_app(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    api.add_namespace(dataNS)
    api.add_namespace(contentNS)


    flask_app.register_blueprint(blueprint)
    db.app = flask_app
    db.init_app(flask_app)

initialize_app(app)


def main():

    app.run(debug=settings.FLASK_DEBUG,port=5010)

if __name__ == "__main__":
    main()
