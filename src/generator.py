"""
Generates synthetic network flow data using the trained LSTM model.
"""
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib

from config import MODELS_DIR, PROCESSED_FLOWS_DIR, SEQUENCE_LENGTH

def generate_synthetic_traffic(mode_label, num_packets_to_generate=1000):
    """
    Uses a trained LSTM to generate new synthetic packet sizes and arrival times.
    """
    model_path = MODELS_DIR / f"{mode_label}_lstm_model.h5"
    scaler_path = MODELS_DIR / f"{mode_label}_scaler.pkl"
    
    print(f"Loading model from {model_path}...")
    try:
        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
    except FileNotFoundError:
        print(f"Error: Model or scaler for '{mode_label}' not found. Run train.py first.")
        return None

    print(f"Generating {num_packets_to_generate} synthetic packets for mode: {mode_label}...")
    
    # 1. Create a "Seed"
    # The LSTM needs a starting sequence to kick off its predictions. 
    # We will use an array of zeros (representing a quiet network state) to start.
    # Shape: (1 batch, SEQUENCE_LENGTH timesteps, 2 features [Size, IAT])
    current_sequence = np.zeros((1, SEQUENCE_LENGTH, 2))
    
    synthetic_data = []

    # 2. Generation Loop
    for _ in range(num_packets_to_generate):
        # Ask the model to predict the next packet based on the current sequence
        next_packet_pred = model.predict(current_sequence, verbose=0)
        
        # Save the prediction
        synthetic_data.append(next_packet_pred[0])
        
        # Update the sequence: slide the window forward
        # Remove the oldest packet (index 0) and append the new prediction at the end
        next_packet_pred_reshaped = np.reshape(next_packet_pred, (1, 1, 2))
        current_sequence = np.append(current_sequence[:, 1:, :], next_packet_pred_reshaped, axis=1)

    # 3. Undo the Scaling
    # The neural network outputs numbers between 0 and 1. We need real bytes and seconds.
    synthetic_data_scaled_back = scaler.inverse_transform(synthetic_data)
    
    # 4. Cleanup and Formatting
    df_synthetic = pd.DataFrame(synthetic_data_scaled_back, columns=['Packet_Size', 'IAT'])
    
    # Neural networks sometimes guess negative numbers if unsure; force them to be at least 0
    df_synthetic['Packet_Size'] = df_synthetic['Packet_Size'].clip(lower=40).astype(int) # Min IPv4 header size
    df_synthetic['IAT'] = df_synthetic['IAT'].clip(lower=0.0)
    
    # Save to a new CSV for the Scapy crafter
    output_filename = f"synthetic_{mode_label}_flow.csv"
    output_path = PROCESSED_FLOWS_DIR / output_filename
    df_synthetic.to_csv(output_path, index=False)
    
    print(f"Successfully generated {num_packets_to_generate} packets.")
    print(f"Saved synthetic flow to: {output_path}\n")
    
    return df_synthetic

if __name__ == "__main__":
    # Example usage: Generate 500 packets of synthetic streaming traffic
    # Ensure you have already trained the streaming model!
    generate_synthetic_traffic(mode_label="streaming", num_packets_to_generate=500)