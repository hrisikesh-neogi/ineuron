import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, Lasso, RidgeCV, LassoCV, ElasticNet, ElasticNetCV, LinearRegression
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import pickle

class train_model:
    def features(self):
        
        global df, x,y 
        df = pd.read_csv('ai4i2020.csv')
        x = df.drop(columns=['UDI', 'Product ID', 'Type','Air temperature [K]' ])
        y = df[['Air temperature [K]']]

    def training(self):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.25, random_state=100)
        lr = LinearRegression()
        lr.fit(x_train, y_train)
        pickle.dump(lr, open('air_temp.pickle', 'wb'))
        
        

def execution_of_model(val):
    train = train_model()
    train.features()
    train.training()    
    model = pickle.load(open('air_temp.pickle', 'rb'))
    value = [np.array(val)]
    predict_data = model.predict(value) 
    # return f'the air temperature is {int(predict_data)}' 
    return ('%.2f'%predict_data)     