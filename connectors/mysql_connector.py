from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

username = 'root'
password = '2727'
host = '127.0.0.1'
database_name = 'milestone_4_smmuja'

# username = os.getenv('DB_USERNAME')
# password = os.getenv('DB_PASSWORD')
# host = os.getenv('DB_HOST')
# database_name = os.getenv('DB_NAME')

ConnectionString = f'mysql+mysqlconnector://{username}:{password}@{host}/{database_name}'
engine = create_engine(ConnectionString)

connection = engine.connect()
Session = sessionmaker(connection)

print('Success connecting to SQL Database')