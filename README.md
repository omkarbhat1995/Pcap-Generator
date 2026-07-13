# Synthetic PCAP Generator

This project builds machine learning models capable of generating realistic synthetic network data in PCAP format. The system simulates various user behaviors to generate traffic that reflects specific modes, such as office work, streaming shows/movies, or gaming.

## System Architecture

Machine learning models struggle to generate raw, byte-by-byte binary PCAP files due to strict protocol rules (e.g., checksums, sequence numbers). To solve this, the system decouples behavior generation from packet packaging:

1. **The ML Model (Behavior):** Learns and generates flow statistics and metadata (packet sizes, inter-arrival times, burst rates, etc.) for specific user behaviors.
2. **The Packet Crafter (Packaging):** Uses `scapy` to ingest the generated statistics and build mathematically valid PCAP files with correct checksums, headers, and handshakes.

## Repository Structure

* `data/raw_pcaps/`: Baseline PCAPs of real gaming, streaming, and office work (Not tracked in Git).
* `data/processed_flows/`: Extracted time-series CSV data used for ML training.
* `models/`: Saved ML models (e.g., TimeGAN, LSTMs).
* `notebooks/`: Jupyter notebooks for data exploration and model testing.
* `src/feature_extractor.py`: Parses real PCAPs into ML-readable time-series data.
* `src/train.py`: Code to train the sequential machine learning models.
* `src/generator.py`: Uses the trained model to output artificial packet arrays and time delays.
* `src/pcap_crafter.py`: Scapy script that takes ML output and constructs valid `.pcap` files.

## Dataset and Acknowledgements

The data used to train the machine learning models in this project is sourced from the **UNB ISCX VPN-nonVPN Dataset (2016)**. 

The ISCXVPN2016 dataset is publicly available for researchers. If you are using this dataset, please cite their related research paper which outlines the details of the dataset and its underlying principles:

> Gerard Drapper Gil, Arash Habibi Lashkari, Mohammad Mamun, Ali A. Ghorbani, "Characterization of Encrypted and VPN Traffic Using Time-Related Features", In Proceedings of the 2nd International Conference on Information Systems Security and Privacy(ICISSP 2016) , pages 407-414, Rome, Italy.

## Getting Started

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and install dependencies: `pip install -r requirements.txt`
4. Place your baseline network captures into `data/raw_pcaps/`.