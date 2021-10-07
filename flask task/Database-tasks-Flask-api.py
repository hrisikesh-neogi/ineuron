import mysql.connector as connection
import os
import logging as lg
from flask import Flask, render_template, request, jsonify
import csv
lg.basicConfig(filename='rishiLOG.log', level=lg.INFO, format='%(asctime)s %(message)s')
app = Flask(__name__)



class sql_db_operation:
    def __init__(self, host, user, password, database, tab):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.tab = tab


    def sql_create_table(self, tab_columns):
        mydb = connection.connect(host=self.host, user=self.user, database=self.database, passwd=self.password, use_pure=True)
        if mydb.is_connected() == True:
            lg.info("database conencted with class")
            # creating table in sql
            cursor = mydb.cursor()
            query = f"create table {self.tab}({tab_columns});"
            cursor.execute(query)
            lg.info('table created with class') 



    def sql_insert(self, values):
        mydb = connection.connect(host=self.host, user=self.user, database=self.database, passwd=self.password, use_pure=True)
        if mydb.is_connected() == True:
            val = tuple(values)
            cursor = mydb.cursor()
            query = f"INSERT INTO {self.database}.{self.tab} values {val};"
            cursor.execute(query)
            mydb.commit()
            lg.info('data inserted into table')

    def update_table(self, condition):
        mydb = connection.connect(host=self.host, user=self.user, database=self.database, passwd=self.password, use_pure=True)
        cursor = mydb.cursor()
        query = f"Update {self.tab} {condition};"
        lg.info(query)
        cursor.execute(query)
        mydb.commit()
        lg.info(f'{self.tab} table updated ')

    def bulk_in(self, path, column):
        mydb = connection.connect(host=self.host, user=self.user, database=self.database, passwd=self.password, use_pure=True)
        # list_of_col = []
        # for key in column:
        #     a = str(key) + ' ' + str(column[key])
        #     list_of_col.append(a)
        # for i in range(1, len(list_of_col)):
        #     list_of_col[0] += ', '+list_of_col[i]
        # col = list_of_col[0]
        cur = mydb.cursor()
        query = f"create table if not exists {self.database}.{self.tab}({column});"   # creating tables in database
        cur.execute(query)
        db = self.database
        tab = self.tab
        with open(str(path), 'r') as data:           # giving the path, this opens the file and commit to the database
            file = csv.reader(data, delimiter=',')
            next(file)
            cur = mydb.cursor()
            for i in file:
                query = f"insert into {db}.{tab} values({', '.join([value for value in i])});"
                cur.execute(query)
        mydb.commit()
        lg.info(f'all data inserted into {db}.{tab}')

    def delete_from_table(self, condition):
        mydb = connection.connect(host=self.host, user=self.user, database=self.database, passwd=self.password, use_pure=True)
        cursor = mydb.cursor()
        query = f"DELETE from {self.database}.{self.tab} {condition};"
        cursor.execute(query)
        mydb.commit()
        result = f' row deleted from {self.database}.{self.tab} {condition}'
        lg.info(result)
        return jsonify(result)

    def download_data(self):
        mydb = connection.connect(host=self.host, user=self.user, database=self.database, passwd=self.password, use_pure=True)
        cur = mydb.cursor()
        query = f"show fields from {self.database}.{self.tab}"
        cur.execute(query)
        a = cur.fetchall()
        list_of_headers= []
        for i in a:
            p = list(i)
            list_of_headers.append(p[0])
            print(list_of_headers)

        list_of_data = []
        list_of_data.append(tuple(list_of_headers))
        cur1 = mydb.cursor()
        query1 = f"Select * from {self.database}.{self.tab};"
        cur1.execute(query1)

        for i in cur1.fetchall():
            list_of_data.append(i)
            print(list_of_data)
        with open ('data downloaded from SQL.csv', 'w', newline='\n') as file:
            f = csv.writer(file)
            f.writerows(list_of_data)
            result = 'row has been downloaded'
            lg.info(result)
            print(result)
            return jsonify(result)









# ROUTES -- API FOR MySQL


@app.route('/sql/sql_create_table', methods=['POST'])   # creating table in MySql db
def sql_db_create_table():
    if (request.method=='POST'):
        host = str(request.json['host'])
        user = str(request.json['user'])
        password = str(request.json['password'])
        database = str(request.json['database'])
        tab = str(request.json['tab'])
        tab_columns = str(request.json['tab_columns'])
        DB = sql_db_operation(host, user, password, database, tab)
        DB.sql_create_table(tab_columns)
        lg.info('using class object route has been initialised and connected to mysql')
        return jsonify('database connected and table created')


@app.route('/sql/insert_into_Table', methods = ['POST'])   # inserting data into table in MySql
def sql_db_insert_val():
    if (request.method=='POST'):
        host = str(request.json['host'])
        user = str(request.json['user'])
        password = str(request.json['password'])
        database = str(request.json['database'])
        tab = str(request.json['tab'])
        val = str(request.json['val'])
        values = list(val.split(","))
        #return jsonify(values)
        for i in values:
            if type(i) == str:
                values[values.index(i)] = int(i)
        #return jsonify(values)

        DB = sql_db_operation(host, user, password, database, tab)
        DB.sql_insert(values)
        result = f'data{values} inserted into tab: {tab}'
        return jsonify(result)


@app.route('/sql/update_table', methods=['POST'])     # updating table in mySql
def update_table():
    if (request.method == 'POST'):
        host = str(request.json['host'])
        user = str(request.json['user'])
        password = str(request.json['password'])
        database = str(request.json['database'])
        tab = str(request.json['tab'])
        condition = str(request.json['condition'])
        DB = sql_db_operation(host, user, password, database, tab)
        DB.update_table(condition)
        lg.info(f'table {tab} updated' )
        result = f'table: {tab} updated'
        return jsonify(result)


@app.route('/sql/bulk_insert', methods=['POST'])    # inserting bulk data into MySQL
def bulk_insert():
    try:
        if (request.method == 'POST'):
            host = str(request.json['host'])
            user = str(request.json['user'])
            password = str(request.json['password'])
            database = str(request.json['database'])
            tab = str(request.json['tab'])
            path = str(request.json['path'])
            column = str(request.json['column'])
            DB = sql_db_operation(host, user, password, database, tab)
            DB.bulk_in(path, column)
            result = f'bulk values have been inserted into {database}.{tab}'
            lg.info(result)
            return jsonify(result)
    except Exception as e:
        print('error occured' , e)
        lg.info(e)


@app.route('/sql/delete_from', methods = ['POST'])
def delete_from():
    try:
        if(request.method == 'POST'):
            host = str(request.json['host'])
            user = str(request.json['user'])
            password = str(request.json['password'])
            database = str(request.json['database'])
            tab = str(request.json['tab'])
            condition = str(request.json['condition'])
            DB = sql_db_operation(host, user, password, database, tab)
            DB.delete_from_table(condition)
            result = f' row deleted from {database}.{tab} {condition}'
            lg.info(result)
            return jsonify(result)

    except Exception as e:
        print('error occured: ', e)
        lg.info(e)
        return jsonify(e)


@app.route('/sql/download_data', methods = ['POST'])
def download_data():
    try:
        if(request.method =='POST'):
            host = str(request.json['host'])
            user = str(request.json['user'])
            password = str(request.json['password'])
            database = str(request.json['database'])
            tab = str(request.json['tab'])
            DB = sql_db_operation(host, user, password, database, tab)
            DB.download_data()
            result = f' data downloaded from {database}.{tab}'
            lg.info(result)
            return jsonify(result)

    except Exception as e:
        lg.info('error occured: ',e)
        return jsonify(e)



# cassandra

import cassandra
import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class cass_operation:
    def __init__(self, zipp, client_id, client_secret,keyspace, tab):
        self.zip = zipp
        self.client_id = client_id
        self.client_secret = client_secret
        self.keyspace = keyspace
        self.tab = tab

    def create_tab_connect(self,  column):     #table creation and db conenction in cassandra

        cloud_config = {
            'secure_connect_bundle': str(self.zip)
        }
        auth_provider = PlainTextAuthProvider(str(self.client_id),
                                              str(self.client_secret))
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect(str(self.keyspace))
        query = f" CREATE TABLE {self.tab}({column});"

        row = session.execute(query).one()
        print(row)
        print('database connected and table created')
        lg.info(f'cassandra db:'+
                f'\n database connected and {self.tab} has been created')

    def cass_insert_data(self, column,val):  #inserting data to cass db
        cloud_config = {
            'secure_connect_bundle': str(self.zip)
        }
        auth_provider = PlainTextAuthProvider(str(self.client_id),
                                              str(self.client_secret))
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect(str(self.keyspace))
        query = f" insert into {self.tab} ({column}) values({val});"

        row = session.execute(query).one()
        print(row)
        print(f'{val} are inserted into {self.keyspace}.{self.tab}')
        lg.info(f'cassandra db:'+
                f'\n {val} are inserted into {self.keyspace}.{self.tab}')

    def cass_update_tab(self, set_condition, where_condition):       # cass tab update
        cloud_config = {
            'secure_connect_bundle': str(self.zip)
        }
        auth_provider = PlainTextAuthProvider(str(self.client_id),
                                              str(self.client_secret))
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect(str(self.keyspace))
        query = f"UPDATE {self.keyspace}.{self.tab} SET {set_condition} WHERE {where_condition};"

        row = session.execute(query).one()
        result = f'{self.keyspace}.{self.tab} is updated successfuly'
        print(result)
        lg.info(result)

    def cass_bulk_up(self, path, columns ):

        cloud_config = {
            'secure_connect_bundle': str(self.zip)
        }
        auth_provider = PlainTextAuthProvider(str(self.client_id),
                                              str(self.client_secret))
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)

        if type(columns) == dict:
            col_n_col_type = []
            for key, value in columns.items():
                col_n_col_type.append(key + ' ' + value)

            session = cluster.connect(str(self.keyspace))
            qry = f"CREATE TABLE IF NOT EXISTS {self.keyspace}.{self.tab} ({', '.join([i for i in col_n_col_type])});"
            print(qry)
            session.execute(qry)
            result = f'{self.keyspace}.{self.tab} has been created'
            lg.info(result)
            print(result)

        # inserting data from csv

        col = []
        for key, values in columns.items():
            col.append(key)

        with open(str(path), 'r') as data:
            file = csv.reader(data, delimiter=',')
            next(file)
            for i in file:
                query = f" insert into {self.keyspace}.{self.tab} ({', '.join([i for i in col])}) values({', '.join([value for value in i])});"
                session.execute(query)
                print(f'data{[value for value in i]} is inserted')
            lg.info(f'data has been inserted into {self.keyspace}.{self.tab}')


    def delete_cass(self, condition):
        cloud_config = {
            'secure_connect_bundle': str(self.zip)
        }
        auth_provider = PlainTextAuthProvider(str(self.client_id),
                                              str(self.client_secret))
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect(str(self.keyspace))
        query = f"DELETE FROM {self.keyspace}.{self.tab} {condition};"

        row = session.execute(query).one()
        result = f'row {condition} has been deleted from {self.keyspace}.{self.tab}'
        print(result)
        lg.info(result)


    def download_data(self, path):
        cloud_config = {
            'secure_connect_bundle': str(self.zip)
        }
        auth_provider = PlainTextAuthProvider(str(self.client_id),
                                              str(self.client_secret))
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect(str(self.keyspace))
        query = f"select * from {self.keyspace}.{self.tab};"
        exe = session.execute(query)
        col = exe.column_names
        c1 = []
        for i in exe:
            c1.append(i)

        c = []
        c.append(col)
        for i in c1:
            c2 = []
            for j in range(0, len(c1) + 1):
                c2.append(i[j])

            c.append(c2)
        with open(path, 'w', newline='\n') as file:
            f = csv.writer(file)
            f.writerows(c)
            result = 'file has been downloaded'
            lg.info(result)
            print(result)
            return jsonify(result)

        # result = f'row {condition} has been deleted from {self.keyspace}.{self.tab}'
        # print(result)
        # lg.info(result)







@app.route('/cassandra/create_table', methods=['POST'])
def db_Connect():
    try:
        if(request.method=='POST'):
            zip= str(request.json['zip'])
            client_Id= str(request.json['client_Id'])
            client_secret= str(request.json['client_secret'])
            tab= str(request.json['tab'])
            keyspace = str(request.json['keyspace'])
            column = str(request.json['column'])
            db = cass_operation(zip, client_Id, client_secret, keyspace, tab)
            db.create_tab_connect( column)
            result = f'database conencted and {tab} is created'
           # print(result,' ',zip,' ',client_Id,' ',client_secret,' ',tab,' ',keyspace,' ', column)
            return jsonify(result)

    except Exception as e:
        print(e)


@app.route('/cassandra/insert_val', methods=['POST'])
def db_insert():
    try:
        if(request.method == 'POST'):
            zip = str(request.json['zip'])
            client_Id = str(request.json['client_Id'])
            client_secret = str(request.json['client_secret'])
            tab = str(request.json['tab'])
            keyspace = str(request.json['keyspace'])
            column = str(request.json['column'])
            val = str(request.json['val'])
            db = cass_operation(zip, client_Id, client_secret,keyspace, tab)
            db.cass_insert_data(column,val)
            result = f'database connected and value {val} is been inserted into {keyspace}.{tab}'
            print(result)
            lg.info(result)
            return jsonify(result)

    except Exception as e:
        print(e)
        lg.info('eror occured', '\n e')
        return jsonify('eror occured', '\n e')


@app.route('/cassandra/update_tab', methods = ['POST'])    #update table in cassandra
def cass_update():
    try:
        if (request.method == 'POST'):
            zip = str(request.json['zip'])
            client_Id = str(request.json['client_Id'])
            client_secret = str(request.json['client_secret'])
            tab = str(request.json['tab'])
            keyspace = str(request.json['keyspace'])
            set_condition = str(request.json['set_condition'])
            where_condition = str(request.json['where_condition'])

            db = cass_operation(zip,client_Id,client_secret,keyspace,tab)
            db.cass_update_tab(set_condition, where_condition)
            result = f'{keyspace}.{tab} is updated successfuly'
            lg.info(result)
            print(result)
            return jsonify(result)

    except Exception as e:
        print('error occured: ', e)
        lg.info(e)


@app.route('/cassandra/bulk_insert', methods = ['POST'])
def cass_bulk_insert():
    try:
        if (request.method == 'POST'):
            zip = str(request.json['zip'])
            client_Id = str(request.json['client_Id'])
            client_secret = str(request.json['client_secret'])
            tab = str(request.json['tab'])
            keyspace = str(request.json['keyspace'])
            column = request.json['column']
            path = str(request.json['path'])
            db = cass_operation(zip, client_Id, client_secret, keyspace, tab)
            db.cass_bulk_up(path, column )
            result = f'data inserted into {keyspace}.{tab}'
            lg.info(result)
            print(result)
            return jsonify(result)

    except Exception as e:
        print('error occured: ', e)
        lg.info(e)


@app.route('/cassandra/delete', methods = ['POST'])

def delete_from_cass():
    try:
        if(request.method == 'POST'):
            zip = str(request.json['zip'])
            client_Id = str(request.json['client_Id'])
            client_secret = str(request.json['client_secret'])
            tab = str(request.json['tab'])
            keyspace = str(request.json['keyspace'])
            condition = str(request.json['condition'])
            DB = cass_operation(zip, client_Id, client_secret,keyspace, tab)
            DB.delete_cass(condition)
            result = f'row {condition} has been deleted from {keyspace}.{tab}'
            print(result)
            lg.info(result)
            return jsonify(result)

    except Exception as e:
        print(str(e))
        return jsonify(str(e))


@app.route('/cassandra/download_Data', methods =['POST'])
def down_cass():
    try:
        if(request.method=='POST'):
            zip = str(request.json['zip'])
            client_Id = str(request.json['client_Id'])
            client_secret = str(request.json['client_secret'])
            tab = str(request.json['tab'])
            keyspace = str(request.json['keyspace'])
            path = str(request.json['path'])
            db = cass_operation(zip, client_Id,client_secret, keyspace, tab)
            db.download_data(path)
            return jsonify(f'data downloaded and downloaded in the location: {path}')


    except Exception as e:
        print(str(e))
        return jsonify(str(e))



#for mongodb
import os
import pandas as pd
import pymongo
import json


class mongo_operation:
    def __init__(self, client_url, db):
        self.client_url = client_url
        self.db = db


    def create_collection(self, collection_name, record, insert_no):
        client = pymongo.MongoClient(self.client_url)
        db = client[self.db]

        collection = db[str(collection_name)]
        if insert_no == 1:
            collection.insert_one(record)
            print(f'{insert_no}record has been inserted')
            lg.info(f'{insert_no} record has been inserted')
        else:
            collection.insert_many(record)
            print(f'{insert_no} records has been inserted')
            lg.info(f'{insert_no} records has been inserted')

    def bulk_insert(self, path, collection_name):
        mng_client = pymongo.MongoClient(self.client_url)
        mng_db = mng_client[self.db]
        db_cm = mng_db[collection_name]

        data = pd.read_csv(path)
        data_json = json.loads(data.to_json(orient='records'))
        db_cm.insert(data_json)
        print('data inserted ')
        lg.info('data inserted successfully')


# api for mongodb
@app.route('/mongo/create_collection', methods = ['POST'])
def create_collection():
    try:
        if(request.method== 'POST'):
            client_url = str(request.json['client_url'])
            collection_name = str(request.json['collection_name'])
            record = request.json['record']
            insert_no = int(request.json['insert_no'])
            database = str(request.json['database'])
            db = mongo_operation(client_url, database)
            db.create_collection(collection_name,record,insert_no)
            result = f'{insert_no} record is inserted'
            lg.info(result)
            print(result)
            return jsonify(result)

    except Exception as e:
        print('error occured:', str(e))
        lg.info('error occured:'+' '+str(e))
        return jsonify('error occured:'+' '+str(e))



@app.route('/mongo/bulk_up', methods = ['POST'])
def bulk_up():
    try:
        if(request.method== 'POST'):
            client_url = str(request.json['client_url'])
            collection_name = str(request.json['collection_name'])
            database = str(request.json['database'])
            path = str(request.json['path'])
            db = mongo_operation(client_url, database)
            db.bulk_insert(path, collection_name)
            print('data inserted ')
            lg.info('data inserted successfully')
            return jsonify('data inserted successfully')

    except Exception as e:
        print('error occured:', str(e))
        lg.info('error occured:'+' '+str(e))
        return jsonify('error occured:'+' '+str(e))




if __name__ == '__main__':
    app.run()




