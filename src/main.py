from data_generator import generate_cold_chain_data
from preprocessing import preprocess_iot_data, create_sequences
from model_architecture import build_lstm_model
from agent_logic import ColdChainAgent
import matplotlib.pyplot as plt
import os

def run_pipeline():
    # 1. Ensure Data exists
    if not os.path.exists('dataset/sample_iot_stream.csv'):
        os.makedirs('dataset', exist_ok=True)
        generate_cold_chain_data()

    # 2. Preprocess
    print("Preprocessing IoT Streams...")
    data, scaler = preprocess_iot_data('dataset/sample_iot_stream.csv')
    X, y = create_sequences(data)

    # 3. Build/Initialize Model
    print("Initializing LSTM Predictive Engine...")
    model = build_lstm_model(input_shape=(X.shape[1], X.shape[2]))

    weights_path = 'results/model_weights.weights.h5'

    # Explicitly build the model so weights are created in memory
    # None represents the 'batch size', which can vary
    model.build(input_shape=(None, X.shape[1], X.shape[2]))

    # Ensure the results directory exists
    os.makedirs('results', exist_ok=True)

    if os.path.exists(weights_path) and os.path.getsize(weights_path) > 0:
        print("Loading pre-trained weights from results/ folder...")
        model.load_weights(weights_path)
    else:
        print("Pre-trained weights not found. Training model now...")
        # We use a small number of epochs for the demo/simulation
        model.fit(X, y, epochs=10, batch_size=32, verbose=1)
        model.save_weights(weights_path)
        print(f"Training complete. Weights saved to {weights_path}")
    
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

    # 6. Save the trained intelligence
    os.makedirs('results', exist_ok=True)
    model.save_weights('results/model_weights.weights.h5')
    print("Model weights saved to results/model_weights.weights.h5")
    print(f"Weights saved. File size: {os.path.getsize(weights_path)} bytes")

    # 7. Generate and Save the Visual Proof
    os.makedirs('results/output_plots', exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(data[-50:, 0], label='Actual Temp (Historical)')
    plt.axhline(y=5.0, color='r', linestyle='--', label='Critical Threshold (5°C)')
    plt.scatter(len(data[-50:]) + 1, predicted_temp, color='green', label='AI Prediction', zorder=5)
    plt.title('Cold-Chain Thermal Excursion Forecast')
    plt.ylabel('Temperature (°C)')
    plt.legend()

    plt.savefig('results/output_plots/thermal_excursion_forecast.png')
    print("Research plot saved to results/output_plots/thermal_excursion_forecast.png")

if __name__ == "__main__":
    run_pipeline()
