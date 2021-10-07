from flask import Flask, render_template, request
import numpy as np

import training_model
# from db import cass_operation

# variables 

table = 'mldlrishipract25'
column = {'Air_temperature': 'decimal PRIMARY KEY', 'Process_temperature ':'decimal', 'Rotational_speed ':'decimal','Torque':'decimal', 'Tool_wear':'decimal',' Machine_failure' :'decimal', 'TWF':'decimal', 'HDF':'decimal','PWF':'decimal', 'OSF' :'decimal', 'RNF' :'decimal'}
zip_loc = "E:\secure-connect-rishi.zip"
client_id =  'ORkTvQTctPzoKWUeQdqaIURv' 
client_secret =  'SwbMx3mpJdn,0gYpy-v8J2ZBwEp3xXZlsB30gNZ8lwGeuc6EQCrhqU+bszz16RBYuygxzK-y1FkNROyS,ljSZhXxT1r6_6So20y.tyGMqv.Gc,E3xUl1-w2,l9fzhZo4'
keyspace = 'ml'

""" redirect,url_for,jsonify"""

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():

    return render_template('index.html')

@app.route('/prediction_data', methods=['POST', 'GET'])
def getval():
    if request.method == 'POST':
        val = [float(i) for i in request.form.values()]
        predict = training_model.execution_of_model(val)
        val.insert(0, float(predict))
        print (f' the val is : {val}')
        # database = cass_operation(val,table,column, zip_loc)
        # database.cass_insert_data()
        # print ('val',':', val, '/', 'predict',':', predict,'/' )
        

        
    return render_template('results.html', Predict =predict)

    


        

        


if __name__ == '__main__':
    app.run(debug=True)