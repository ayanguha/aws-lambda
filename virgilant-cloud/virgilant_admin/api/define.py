import traceback
from flask import request,render_template,make_response,jsonify,redirect,url_for


from flask_restplus import Api
import virgilant_admin.settings
from sqlalchemy.orm.exc import NoResultFound


api = Api(version='1.0', title='Virgilant Admin API',doc='/doc/',
          description='Virgilant Data Management API')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    return {'message':message},500

    #return make_response(
              #render_template('TokenError.html',
                              #msg=message
                            #),500,{})




@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    return {'message': 'A database result was required but none was found.'}, 404
