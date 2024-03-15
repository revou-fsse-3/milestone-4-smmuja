from flask import Blueprint, render_template, request
from connectors.mysql_connector import Session

from models.transaction import Transaction
# from models.user import User
from sqlalchemy import select, or_

from flask_login import current_user, login_required
from decorators.role_checker import role_required

transaction_routes = Blueprint('account_routes', __name__)

@transaction_routes.route('/transaction', methods=['GET'])
# @login_required
# @role_required('Admin')
def transaction_list():
    response_data = dict()

    session = Session()

    try:
        account_query = select(Transaction)

        #Tambahkan filter apabila ada search query
        if request.args.get('query') != None:
            search_query = request.args.get('query')
            transaction_query = transaction_query.where(Transaction.id.like(f'% {search_query} %')) 

        transactions = session.execute(transaction_query)
        transactions = transactions.scalars()
        response_data['transations'] = transactions
        


        # print(products)
    except Exception as e:
        print(e)
        return 'Error Processing Data'

    # response_data['name'] = current_user.name
    return render_template('accounts/account_all.html', response_data = response_data)

@transaction_routes.route("/transactions/<id>", methods=['GET'])
def transaction_detail(id):
    response_data = dict()

    session = Session()

    try:
        transaction = session.query(Transaction).filter((Transaction.id==id)).first()
        if (transaction == None):
            return "Data not found"
        response_data['transaction'] = transaction
    except Exception as e:
        print(e)
        return "Error Processing Data"

    return render_template("accounts/account_all.html", response_data = response_data)


@transaction_routes.route('/transactions', methods=['POST'])
# @role_required('Admin')
def acccount_insert():
    new_transaction = Transaction(
        id = request.form['id'],
        account_type = request.form['accountType'],
        account_number = request.form['accounttNumber'],
        balance = request.form['balance']
        )
    
    session = Session()
    session.begin()
    try:
       session.add(new_transaction)
       session.commit()

        
    except Exception as e:
        #Operation failed
       session.rollback()
       print(e)
       return { 'message': 'Insert data gagal'}

    #Operation sukses
    return {'message': 'Input data sukses'}


@transaction_routes.route('/transactions/<id>', methods=['DELETE'])
def transaction_delete(id):
    session = Session()
    session.begin()

    try:
        transaction_to_delete = session.query(Transaction).filter(Transaction.id==id).first()
        session.delete(transaction_to_delete)
        session.commit()

    except Exception as e:
        session.rollback()
        print(e)
        return{'message': 'Delete Data Gagal'}

    #Operation sukses
    return {'message': 'Delete Data Sukses'}


@transaction_routes.route('/transactions/<id>', methods=['PUT'])
def transaction_update(id):
    session = Session()
    session.begin()

    try:
        transaction_to_update = session.query(Transaction).filter(Transaction.id==id).first()
        
        transaction_to_update.from_account_id = request.form['fromAccountId']
        transaction_to_update.to_account_id = request.form['toAccountId']
        transaction_to_update.amount = request.form['amount']
        transaction_to_update.description = request.form['description']

        session.commit()

    except Exception as e:
        session.rollback()
        print(e)
        return{'message': 'Update Data Gagal'}

    #Operation sukses
    return {'message': 'Update Data Sukses'}
