from data_generator import generate_cold_chain_data
from preprocessing import preprocess_iot_data, create_sequences
from model_architecture import build_lstm_model
from agent_logic import ColdChainAgent
import os

def run_pipeline():
    # 1. Ensure Data exists
    if not os.path.exists('dataset/sample_iot_stream.csv'):
        os.makedirs('dataset', exist_ok=True)
        generate_cold_chain_data()

    # 2. Preprocess
    print("🔄 Preprocessing IoT Streams...")
    data, scaler = preprocess_iot_data('dataset/sample_iot_stream.csv')
    X, y = create_sequences(data)

    # 3. Build/Initialize Model
    print("🧠 Initializing LSTM Predictive Engine...")
    model = build_lstm_model(input_shape=(X.shape[1], X.shape[2]))
    
    # 4. Predict (Simulating a real-time check)
    last_sequence = X[-1].reshape(1, X.shape[1], X.shape[2])
    predicted_scaled = model.predict(last_sequence)
    
    # Inverse scale to get actual Celsius
    predicted_temp = (predicted_scaled[0][0] * (data[:,0].max() - data[:,0].min())) + data[:,0].min()

    # 5. Agentic Decision
    agent = ColdChainAgent()
    decision = agent.evaluate_action(predicted_temp)

    print("-" * 30)
    print(f"Predicted Temp (Next 4h): {predicted_temp:.2f}°C")
    print(f"Agentic Decision: {decision}")
    print("-" * 30)

if __name__ == "__main__":
    run_pipeline()
