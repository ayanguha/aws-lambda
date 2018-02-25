import traceback

from flask_restplus import Api
import virgilant.settings
from sqlalchemy.orm.exc import NoResultFound


api = Api(version='1.0', title='Virgilant API',
          description='Virgilant Data Management API')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not virgilant.settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    return {'message': 'A database result was required but none was found.'}, 404
