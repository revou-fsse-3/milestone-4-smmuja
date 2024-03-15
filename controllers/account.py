from flask import Blueprint, render_template, request
from connectors.mysql_connector import Session

from models.account import Account
# from models.user import User
from sqlalchemy import select, or_

from flask_login import current_user, login_required
from decorators.role_checker import role_required

account_routes = Blueprint('account_routes', __name__)

@account_routes.route('/accounts', methods=['GET'])
@login_required
# @role_required('Admin')
def account_list():
    response_data = dict()

    session = Session()

    try:
        account_query = select(Account)

        #Tambahkan filter apabila ada search query
        if request.args.get('query') != None:
            search_query = request.args.get('query')
            account_query = account_query.where(Account.id.like(f'% {search_query} %')) 

        accounts = session.execute(account_query)
        accounts = accounts.scalars()
        response_data['accounts'] = accounts
        


        # print(products)
    except Exception as e:
        print(e)
        return 'Error Processing Data'

    # response_data['name'] = current_user.name
    return render_template('accounts/account_all.html', response_data = response_data)

@account_routes.route("/accounts/<id>", methods=['GET'])
@login_required
def account_detail(id):
    response_data = dict()

    session = Session()

    try:
        account = session.query(Account).filter((Account.id==id)).first()
        if (account == None):
            return "Data not found"
        response_data['account'] = account
    except Exception as e:
        print(e)
        return "Error Processing Data"

    return render_template("accounts/account_all.html", response_data = response_data)


@account_routes.route('/accounts', methods=['POST'])
# @role_required('Admin')
@login_required
def acccount_insert():
    new_account = Account(
        id = request.form['id'],
        account_type = request.form['accountType'],
        account_number = request.form['accounttNumber'],
        balance = request.form['balance']
        )
    
    session = Session()
    session.begin()
    try:
       session.add(new_account)
       session.commit()

        
    except Exception as e:
        #Operation failed
       session.rollback()
       print(e)
       return { 'message': 'Insert data gagal'}

    #Operation sukses
    return {'message': 'Input data sukses'}


@account_routes.route('/accounts/<id>', methods=['DELETE'])
def account_delete(id):
    session = Session()
    session.begin()

    try:
        account_to_delete = session.query(Account).filter(Account.id==id).first()
        session.delete(account_to_delete)
        session.commit()

    except Exception as e:
        session.rollback()
        print(e)
        return{'message': 'Delete Data Gagal'}

    #Operation sukses
    return {'message': 'Delete Data Sukses'}


@account_routes.route('/accounts/<id>', methods=['PUT'])
def account_update(id):
    session = Session()
    session.begin()

    try:
        account_to_update = session.query(Account).filter(Account.id==id).first()
        
        account_to_update.id = request.form['id']
        account_to_update.account_type = request.form['accountType']
        account_to_update.balance = request.form['balance']

        session.commit()

    except Exception as e:
        session.rollback()
        print(e)
        return{'message': 'Update Data Gagal'}

    #Operation sukses
    return {'message': 'Update Data Sukses'}
