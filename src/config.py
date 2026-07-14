"""
src/config.py
Central configuration for paths, model parameters, and network settings.
"""
import os
from pathlib import Path

# --- Directory Setup ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_PCAP_DIR = DATA_DIR / "raw_pcaps"
PROCESSED_FLOWS_DIR = DATA_DIR / "processed_flows"
MODELS_DIR = PROJECT_ROOT / "models"

for d in [RAW_PCAP_DIR, PROCESSED_FLOWS_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- Network Modes & File Routing ---
MODES = ["working", "streaming", "gaming"]

# These substrings map the raw ISCX file names to our target profiles
FILE_MAPPINGS = {
    "working": ["email", "ftps", "gmail", "hangouts", "facebook", "icq", "aim"],
    "streaming": ["netflix", "youtube", "vimeo"],
    "gaming": [] # Placeholder: Needs external data (e.g., LORIA dataset)
}

# --- ML Extraction Parameters ---
SEQUENCE_LENGTH = 100