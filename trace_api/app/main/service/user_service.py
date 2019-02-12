import datetime
import uuid

from app.main import db
from app.main.model.tables import User


def save_new_user(data):
    user = User.query.filter_by(Email=data['email']).first()
    if not user:
        new_user = User(
            PublicID=str(uuid.uuid4()),
            Email=data['email'],
            Admin=data['admin'],
            Username=data['username'],
            password=data['password'],
            RegisteredOn=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(PublicID=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.ID)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
