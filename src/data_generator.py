import pandas as pd
import numpy as np
import datetime

def generate_cold_chain_data(hours=24, interval_min=5):
    """Generates synthetic IoT sensor data for a refrigerated container."""
    intervals = (hours * 60) // interval_min
    start_time = datetime.datetime.now()
    
    # Base parameters for "Fresh Produce" (e.g., Berries)
    base_temp = 2.0  # Celsius
    base_humidity = 90.0
    base_co2 = 400.0
    
    data = []
    for i in range(intervals):
        current_time = start_time + datetime.timedelta(minutes=i * interval_min)
        
        # Add normal sensor noise
        temp = base_temp + np.random.normal(0, 0.2)
        hum = base_humidity + np.random.normal(0, 1.0)
        co2 = base_co2 + np.random.normal(0, 10.0)
        
        # INJECT FAILURE: After 12 hours, simulate a compressor malfunction
        if i > (intervals // 2):
            temp += (i - (intervals // 2)) * 0.15 # Steady rise in temp
            
        data.append([current_time, temp, hum, co2])
    
    df = pd.DataFrame(data, columns=['Timestamp', 'Temperature', 'Humidity', 'CO2'])
    df.to_csv('dataset/sample_iot_stream.csv', index=False)
    print("✅ Synthetic Cold-Chain Dataset Generated: dataset/sample_iot_stream.csv")

if __name__ == "__main__":
    generate_cold_chain_data()
