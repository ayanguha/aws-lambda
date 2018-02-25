from virgilant.database import db
from virgilant.database.models import *
from flask import Response
from sqlalchemy.orm.exc import NoResultFound

from flask_restplus import reqparse

user_action = reqparse.RequestParser()
user_action.add_argument('action',  required=True,  choices=['optin', 'optout', 'activate', 'deactivate'], help='User action')


def getAllUsers(n):
    #return jsonify(user_list=[i.serialize for i in User.query.all()])
    return [i.serialize for i in User.query.limit(n).all()]

def createUser(request):
    u = User(request.form)
    db.session.add(u)
    db.session.commit()
    return { "result" :"sucessfully added user"}

def updateOneUser(user_id,request):
    u = User.query.get(user_id)
    if u:
        if request.form.has_key('location'):
            u.location = request.form['location']
        db.session.commit()
        return { "result" :"sucessfully updated user"}
    else:
        raise NoResultFound

def ActiionOneUserHandler(user_id,args):
    u = User.query.get(user_id)
    if u:
        if args.get('action','activate') == 'activate':
            u.is_active = True
            resp = { "result" :"sucessfully activated user"}
        elif args.get('action','activate') == 'deactivate':
            u.is_active = False
            resp = { "result" :"sucessfully deactivated user"}
        elif args.get('action','activate') == 'optin':
            u.mailing_list_optin = True
            resp = { "result" :"sucessfully opted in"}
        elif args.get('action','activate') == 'optout':
            u.mailing_list_optin = False
            resp = { "result" :"sucessfully opted out"}
        else:
            u.user_id = user_id
            resp = {"result" :"No such option"}
        db.session.commit()
        return { "result" :"sucessfully deactivated user"}
    else:
        raise NoResultFound
