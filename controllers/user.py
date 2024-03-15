from flask import Blueprint, render_template, request, redirect
from connectors.mysql_connector import engine

from models.user import User
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user, current_user

user_routes = Blueprint('user_routes',__name__)

@user_routes.route("/register", methods=['GET'])
def user_register():
    return render_template("auth/register.html")

@user_routes.route("/register", methods=['POST'])
def do_registration():

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    NewUser = User(username=username, email=email)
    NewUser.set_password(password)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session=Session()

    session.begin()

    try:
        # session.add(NewUser)
        # session.commit()

        # user = session.query(User).filter(User.email==request.form['email']).first()

        
        session.add(NewUser)
        session.commit()

        #Check registered email
        # if user.email(request.form['email']):
        #     return {'message': 'Email already registered'}

        # # return {'message': 'Sukses register'}
        # return redirect('/login')

    except Exception as e:
        session.rollback()
        return {'message': 'Gagal Register'}
        # return e
    
    # return {'message': 'Sukses register'}
    return redirect('/login')

@user_routes.route("/login", methods=['GET'])
def user_login():
    return render_template("auth/login.html")

@user_routes.route("/login", methods=['POST'])
def do_user_login():

    response_data = dict()

    connection = engine.connect()
    Session = sessionmaker(connection)
    session=Session()

    try:
        user = session.query(User).filter(User.email==request.form['email']).first()

        if user == None:
            return {'message': 'Email tidak terdaftar'}

        #Check password
        if not user.check_password(request.form['password']):
            return {'message': 'Password salah'}
        

        login_user(user, remember=False)

        response_data['id'] = current_user.id

        
        return redirect ('/users')

        
    except Exception as e:
        return { 'message' : 'Login failed'}
        # return str(e)
    
@user_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return redirect('/login')