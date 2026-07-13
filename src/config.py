"""
Central configuration for paths, model parameters, and network settings.
"""
import os
from pathlib import Path

# --- Directory Setup ---
# Gets the absolute path of the project root (one level up from src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_PCAP_DIR = DATA_DIR / "raw_pcaps"
PROCESSED_FLOWS_DIR = DATA_DIR / "processed_flows"
MODELS_DIR = PROJECT_ROOT / "models"

# Ensure directories exist
for d in [RAW_PCAP_DIR, PROCESSED_FLOWS_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- Network Modes ---
MODES = ["gaming", "streaming", "office"]

# --- ML Extraction Parameters ---
# How many packets to group together to form a "flow sequence" for the LSTM/TimeGAN
SEQUENCE_LENGTH = 100