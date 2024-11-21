import light_pandas as pd
import light_matplotlib.pyplot as plt
from light_stats.tsa.arima.model import ARIMA
from light_stats.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error
import numpy as np
from light_stats.tsa.stattools import adfuller
import pickle
import os

class MyARIMA():
    def __init__(self, data):
        self.data = data.copy()
        self.original_data = data.copy()
        self.data['bulan'] = pd.to_datetime( self.data['bulan'])  # Pastikan kolom tanggal ada
        self.original_data['bulan'] = pd.to_datetime( self.original_data['bulan'])  # Pastikan kolom tanggal ada
        self.data.set_index('bulan', inplace=True)
        self.original_data.set_index('bulan', inplace=True)
        
        self.last_actual_value = self.original_data['penjualan'].iloc[-len(self.original_data) + 1]
        try:
            with open("model.pkl", "rb") as models:
                self.model_fit = pickle.load(models)
        except Exception as E:
            print("Model tidak dapat dimuat !, harap lakukan training terlebih dahulu !")
    
    def dif(self):
        self.data =  self.data.diff().dropna()
        print(self.data)
        
    def checkStationary(self):
        result = adfuller(self.data['penjualan'])
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

        train = self.data[:-len(self.data)+1] 
        test = self.data[-len(self.data)+1:]  

        model = ARIMA(train, order=(p, d, q))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=step)
 
        if not os.path.exists("model.pkl"):
            with open("model.pkl", 'x') as f: pass
            
        with open("model.pkl", "wb") as models:
            pickle.dump(self.model_fit, models)

        rmse = np.sqrt(mean_squared_error(test, forecast))
        print(f'RMSE: {rmse}')
    
    def predict(self, x=1):
        pred = self.model_fit.forecast(steps=x) 
        # plt.figure(figsize=(10, 6))
        # plt.plot(self.data, label='Data Aktual')
        # plt.plot(pred, label='Prediksi', color='red')
        # plt.title('Prediksi Penjualan Parfum Bulanan')
        # plt.xlabel('Waktu')
        # plt.ylabel('Penjualan')
        # plt.legend()
        # plt.show()

        print("Hasil prediksi ")
        print(pred)
        
        inverse_forecast = []
        prev_value = self.last_actual_value
        
        for diff in pred:
            actual_value = prev_value + diff
            inverse_forecast.append(actual_value)
            prev_value = actual_value

        forecast_inverse_df = pd.DataFrame({
            'Tanggal': pred.index,
            'Prediksi Skala Asli': inverse_forecast,
            'Aktual': self.original_data['penjualan'][-len(pred):].values
        })
        
        print(forecast_inverse_df)

        # plt.figure(figsize=(10, 6))
        # plt.plot(self.original_data.index, self.original_data['penjualan'], label='Data Aktual Asli', alpha=0.7)
        # plt.plot(forecast_inverse_df['Tanggal'], forecast_inverse_df['Prediksi Skala Asli'], label='Prediksi (Inverse)', color='red', linestyle='--')
        # plt.title('Prediksi vs Data Aktual pada Skala Asli')
        # plt.xlabel('Waktu')
        # plt.ylabel('Penjualan')
        # plt.legend()
        # plt.show()
        
        return {
            "tanggal" : pred.index,
            "value" : inverse_forecast
        }


data = pd.read_csv('data.csv')  
model = MyARIMA(data)
model.dif()
# if(model.checkStationary()):
#     # model.train(param=(2,1,1))
#     model.predict(10)



