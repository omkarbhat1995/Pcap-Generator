# Synthetic PCAP Generator

[cite_start]This project builds machine learning models capable of generating realistic synthetic network data in PCAP format[cite: 1]. [cite_start]The system simulates various user behaviors to generate traffic that reflects specific modes, such as office work, streaming shows/movies, or gaming[cite: 2].

## System Architecture

[cite_start]Machine learning models struggle to generate raw, byte-by-byte binary PCAP files due to strict protocol rules (e.g., checksums, sequence numbers)[cite: 7, 8]. [cite_start]To solve this, the system decouples behavior generation from packet packaging[cite: 10]:

1. [cite_start]**The ML Model (Behavior):** Learns and generates flow statistics and metadata (packet sizes, inter-arrival times, burst rates, etc.) for specific user behaviors[cite: 10].
2. [cite_start]**The Packet Crafter (Packaging):** Uses `scapy` to ingest the generated statistics and build mathematically valid PCAP files with correct checksums, headers, and handshakes[cite: 11].

## Repository Structure

* [cite_start]`data/raw_pcaps/`: Baseline PCAPs of real gaming, streaming, and office work (Not tracked in Git)[cite: 16].
* `data/processed_flows/`: Extracted time-series CSV data used for ML training.
* [cite_start]`models/`: Saved ML models (e.g., TimeGAN, LSTMs)[cite: 20].
* `notebooks/`: Jupyter notebooks for data exploration and model testing.
* [cite_start]`src/feature_extractor.py`: Parses real PCAPs into ML-readable time-series data[cite: 16, 18].
* [cite_start]`src/train.py`: Code to train the sequential machine learning models[cite: 19].
* [cite_start]`src/generator.py`: Uses the trained model to output artificial packet arrays and time delays[cite: 22, 23].
* [cite_start]`src/pcap_crafter.py`: Scapy script that takes ML output and constructs valid `.pcap` files[cite: 24, 25, 26].

## Getting Started

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and install dependencies: `pip install -r requirements.txt`
4. Place your baseline network captures into `data/raw_pcaps/`.