"""
Synthetic PCAP Generator Package
--------------------------------
This package contains the core modules for extracting network features,
training generative machine learning models, producing synthetic flows, 
and crafting valid PCAP files.
"""

# Optional: You can explicitly define what modules are exposed 
# when someone uses `from src import *`. This keeps the namespace clean.
__all__ = [
    "config",
    "feature_extractor",
    "train",
    "generator",
    "pcap_crafter"
]