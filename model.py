# import sys, os
# sys.path.append(os.path.abspath(os.path.join('lib')))
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

from statsmodels.tsa.stattools import adfuller
import pickle
import os

class MyARIMA():
    def __init__(self, data):
        self.data = data.copy()
        self.original_data = data.copy()
        self.actual = pd.read_csv('aktual.csv')
        self.actual['bulan'] = pd.to_datetime( self.actual['bulan'])
        self.actual.set_index('bulan', inplace=True)
        self.data['bulan'] = pd.to_datetime( self.data['bulan'])  # Pastikan kolom tanggal ada
        self.original_data['bulan'] = pd.to_datetime( self.original_data['bulan'])  # Pastikan kolom tanggal ada
        self.data.set_index('bulan', inplace=True)
        self.original_data.set_index('bulan', inplace=True)
        
        self.last_actual_value = self.original_data['penjualan'].iloc[-len(self.original_data) ].copy()
        print(self.last_actual_value)
        try:
            with open("model.pkl", "rb") as models:
                self.model_fit = pickle.load(models)
        except Exception as E:
            print("Model tidak dapat dimuat !, harap lakukan training terlebih dahulu !")
    
    def dif(self, val):
        self.data =  self.data.diff(val).dropna()
        print(self.data)
        
    def checkStationary(self, data=None):
        if data==None : data = self.data["penjualan"]
        result = adfuller(data)
        print('p-value:', result[1])
        print('ADF Statistic:', result[0])

        if result[1] > 0.05:
            print("Data tidak stasioner, lakukan differencing.")
            return False
        else:
            print("Data sudah stasioner.")
            return True
    
    def train(self, step = 0 , param=(1,1,1)):
        if step == 0 : step = len(self.data)-1
        self.data = self.data.resample('ME').sum()

        plt.figure(figsize=(10, 5))
        plt.plot(self.data, label='Penjualan Bulanan')
        plt.title('Penjualan Parfum Bulanan')
        plt.xlabel('Waktu')
        plt.ylabel('Penjualan')
        plt.legend()
        plt.show()

        plot_acf(self.data)
        plot_pacf(self.data)
        plt.show()

        p, d, q = param 

        self.model = ARIMA(self.data, order=(p, d, q))
        self.model_fit = self.model.fit()
        print(self.model_fit.summary())
        
        residuals = self.model_fit.resid
        plt.figure(figsize=(10, 6))
        plt.plot(residuals, label='Residuals')
        plt.title('Residuals dari Model ARIMA')
        plt.legend()
        plt.show()

        train_size = 10 
        train = self.data[:train_size] 
        test = self.data[train_size:]  

        self.model = ARIMA(train, order=(p, d, q))
        self.model_fit = self.model.fit()
        forecast = self.model_fit.forecast(steps=len(self.data) - train_size)
 
        if not os.path.exists("model.pkl"):
            with open("model.pkl", 'x') as f: pass
            
        with open("model.pkl", "wb") as models:
            pickle.dump(self.model_fit, models)

        rmse = np.sqrt(mean_squared_error(test, forecast))
        mae = mean_absolute_error(test, forecast)
        print(test)
        self.mape = np.mean(np.abs((test["penjualan"] - forecast) / test["penjualan"])) * 100
        
        print(f'RMSE : {rmse}')
        print(f'MAE  : {mae}')
        print(f'MAPE : {self.mape}')
    
    
    def predict(self, x=1):
       
        
        pred = self.model_fit.forecast(steps=x) 
        plt.figure(figsize=(10, 6))
        plt.plot(pred, label='Prediksi', color='red')
        plt.plot(self.actual, label='Data Aktual', color='blue')
        plt.title('Prediksi Penjualan Parfum Bulanan')
        plt.xlabel('Waktu')
        plt.ylabel('Penjualan')
        plt.legend()
        plt.show()

        print("Hasil prediksi ")
        print(pred)
        inverse_forecast = []
        prev_value = self.last_actual_value
        
        return {
            "tanggal" : pred.index,
            "value" : inverse_forecast,
            "mape" : self.mape
        }


data = pd.read_csv('aktual.csv')  
model = MyARIMA(data)
model.train(param=(5,1,1))
model.checkStationary()
model.predict(6)



