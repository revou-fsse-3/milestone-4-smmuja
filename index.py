from flask import Flask
from dotenv import load_dotenv
from connectors.mysql_connector import engine

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from flask_login import LoginManager
from models.user import User
from models.account import Account
import os

from controllers.user import user_routes
from controllers.user_all import users_routes
from controllers.account import account_routes


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    session=Session()

    return session.query(User).get(int(user_id))


    print('Server is starting')

app.register_blueprint(user_routes)
app.register_blueprint(users_routes)
app.register_blueprint(account_routes)

@app.route('/')
def hello_world():

    #Insert using SQL
    # Session = sessionmaker(connection)
    # with Session() as s:
    #     s.execute(text("INSERT INTO product (name, price, description, created_at) VALUES ('Wallet', 15000, 'Create from cow skin', '2024-02-01 00:00:00')"))
    #     s.commit()

    #Insert using model
    # NewProduct = Product(name='Snake Wallet', price=3000, description='Created from Snake Skin', created_at='2024-02-01 00:00:00')
    # Session = sessionmaker(connection)
    # with Session() as s:
    #     s.add(NewProduct)
    #     s.commit()

    # Created at auto default
    # NewProduct = Product(name='Snake Wallet', price=3000, description='Created from Snake Skin')
    # Session = sessionmaker(connection)
    # with Session() as s:
    #     s.add(NewProduct)
    #     s.commit()

    


    # return 'Hello World'


    # Fetch all Products
    # user_query = select(User)
    # Session = sessionmaker(connection)
    # with Session() as session:
    #     result = session.execute(user_query)
    #     for row in result.scalars():
    #         print(f'ID: {row.id}, Name: {row.username}')

    return "<p>Insert Success</p>"