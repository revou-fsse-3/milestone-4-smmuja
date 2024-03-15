from flask import Blueprint, render_template, request
from connectors.mysql_connector import Session

from models.user import User
from sqlalchemy import select, or_

from decorators.role_checker import role_required
from flask_login import current_user, login_required, login_user

users_routes = Blueprint('users_routes', __name__)

@users_routes.route('/users', methods=['GET'])
@login_required
def list_users():
    response_data = dict()

    session = Session()

    try:
        user_query = select(User)

        #Tambahkan filter apabila ada search query
        if request.args.get('query') != None:
            search_query = request.args.get('query')
            user_query = user_query.where(or_(User.username.like(f'% {search_query} %'), User.email.like(f'%{search_query}%'))) 

        users= session.execute(user_query)
        users= users.scalars()
        response_data['users'] = users
        


        # print(users)
    except Exception as e:
        print(e)
        return 'Error Processing Data'

    response_data['username'] = current_user.username
    return render_template('users/user_all.html', response_data = response_data)

# User detail
@users_routes.route('/users/<id>', methods=['GET'])
@login_required
def user_detail(id):
    response_data = dict()

    session = Session()

    try:
        user = session.query(User).filter((User.id==id)).first()
        if (user == None):
            return "Data not found"
        response_data['user'] = user
    except Exception as e:
        print(e)
        return "Error Processing Data"

    response_data['id'] = current_user.id
    response_data['username'] = current_user.username
    response_data['email'] = current_user.email
    response_data['created_at'] = current_user.created_at

    return render_template("users/user_detail.html", response_data = response_data)

#User dashboard after login

@users_routes.route('/users/me', methods=['GET'])
def user_me(id):
    response_data = dict()

    session = Session()

    try:
        user = session.query(User).filter((User.id==id)).first()
        if (user == None):
            return "Data not found"
        response_data['user'] = user
    except Exception as e:
        print(e)
        return "Error Processing Data"

    login_user(user, remember=False)

    response_data['id'] = current_user.id

    return render_template("users/user_detail.html", response_data = response_data)

# Create User
@users_routes.route('/users', methods=['POST'])

def user_insert():
    new_user = User(
        username = request.form['username'],
        email = request.form['email'],
        password = request.form['password']
        )
    
    session = Session()
    session.begin()
    try:
       session.add(new_user)
       session.commit()

        
    except Exception as e:
        #Operation failed
       session.rollback()
       print(e)
       return { 'message': 'Insert data gagal'}

    #Operation sukses
    return {'message': 'Input data sukses'}


@users_routes.route('/users/<id>', methods=['DELETE'])
@role_required('Admin')
def user_delete(id):
    session = Session()
    session.begin()

    try:
        user_to_delete = session.query(User).filter(User.id==id).first()
        session.delete(user_to_delete)
        session.commit()

    except Exception as e:
        session.rollback()
        print(e)
        return{'message': 'Delete Data Gagal'}

    #Operation sukses
    return {'message': 'Delete Data Sukses'}


@users_routes.route('/users/<id>', methods=['PUT'])
@login_required
def user_update(id):
    session = Session()
    session.begin()

    try:
        user_to_update = session.query(User).filter(User.id==id).first()
        
        user_to_update.username = request.form['username']
        user_to_update.email = request.form['email']
        user_to_update.password = request.form['password']

        session.commit()

    except Exception as e:
        session.rollback()
        print(e)
        return{'message': 'Update Data Gagal'}

    #Operation sukses
    return {'message': 'Update Data Sukses'}
