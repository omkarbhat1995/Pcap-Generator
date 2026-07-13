"""
Trains an LSTM model to generate synthetic network flow data.
"""
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import joblib

from config import PROCESSED_FLOWS_DIR, MODELS_DIR, SEQUENCE_LENGTH

def load_and_preprocess_data(mode_label):
    """Loads extracted features and prepares them for the LSTM."""
    file_path = PROCESSED_FLOWS_DIR / f"{mode_label}_processed.csv"
    print(f"Loading data from: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}. Did you run the feature extractor?")
        return None, None, None
        
    # We will focus on predicting Packet_Size and Inter-Arrival Time (IAT)
    # You can expand this to predict Protocol and Direction later using categorical encoding
    features = df[['Packet_Size', 'IAT']].values
    
    # Neural networks perform best when data is scaled between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(features)
    
    # Save the scaler so the generator can reverse the math later!
    scaler_path = MODELS_DIR / f"{mode_label}_scaler.pkl"
    joblib.dump(scaler, scaler_path)
    
    X, y = [], []
    # Create sequences: use 100 packets to predict the 101st packet
    for i in range(SEQUENCE_LENGTH, len(scaled_data)):
        X.append(scaled_data[i-SEQUENCE_LENGTH:i])
        y.append(scaled_data[i])
        
    return np.array(X), np.array(y), scaler

def build_lstm_model(input_shape):
    """Constructs the sequential LSTM architecture."""
    model = Sequential()
    
    # First LSTM layer
    model.add(LSTM(units=64, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2)) # Prevents overfitting
    
    # Second LSTM layer
    model.add(LSTM(units=64, return_sequences=False))
    model.add(Dropout(0.2))
    
    # Output layer (2 neurons: one for Packet_Size, one for IAT)
    model.add(Dense(units=2))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(mode_label, epochs=20, batch_size=64):
    """Main pipeline to load data, build, train, and save the model."""
    X, y, scaler = load_and_preprocess_data(mode_label)
    
    if X is None:
        return
        
    print(f"Training data shape: {X.shape}")
    
    model = build_lstm_model(input_shape=(X.shape[1], X.shape[2]))
    
    print(f"Training the {mode_label} model for {epochs} epochs...")
    model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.1)
    
    # Save the trained model
    model_path = MODELS_DIR / f"{mode_label}_lstm_model.h5"
    model.save(model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    # Example usage: Train the streaming model
    # Ensure 'streaming_processed.csv' exists in data/processed_flows/ first!
    train_model(mode_label="streaming", epochs=10)