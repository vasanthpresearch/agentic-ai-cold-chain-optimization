import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def preprocess_iot_data(file_path):
    """
    Loads and scales IoT data for the LSTM model.
    """
    df = pd.read_csv(file_path)
    
    # Feature Selection: Focus on Temp, Humidity, and CO2
    features = df[['Temperature', 'Humidity', 'CO2']].values
    
    # Scaling data to [0,1] range (essential for Neural Networks)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(features)
    
    return scaled_data, scaler

def create_sequences(data, seq_length=12):
    """
    Converts flat data into 'windows' of time for the LSTM.
    (e.g., use the last 1 hour of data to predict the next 5 mins).
    """
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length, 0]) # Target is Temperature
    return np.array(X), np.array(y)
