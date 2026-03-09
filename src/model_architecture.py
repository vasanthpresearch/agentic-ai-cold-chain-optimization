import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def build_lstm_model(input_shape):
    """
    Defines the LSTM architecture for thermal excursion prediction.
    """
    model = Sequential([
        # First LSTM layer with Dropout to prevent overfitting
        LSTM(units=64, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        
        # Second LSTM layer to capture deeper temporal patterns
        LSTM(units=32, return_sequences=False),
        Dropout(0.2),
        
        # Dense layers to output the predicted temperature
        Dense(units=16, activation='relu'),
        Dense(units=1)  # Predicting the next temperature value
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model
