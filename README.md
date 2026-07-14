# Synthetic PCAP Generator

This project builds machine learning models capable of generating realistic synthetic network data in PCAP format. The system simulates various user behaviors to generate traffic that reflects specific modes: office work, streaming shows/movies, and gaming.

## System Architecture

Machine learning models struggle to generate raw, byte-by-byte binary PCAP files due to strict protocol rules (e.g., checksums, sequence numbers). To solve this, the system decouples behavior generation from packet packaging:

1. **The ML Model (Behavior):** Learns and generates flow statistics and metadata (packet sizes, inter-arrival times, burst rates, etc.) for specific user behaviors.
2. **The Packet Crafter (Packaging):** Uses `scapy` to ingest the generated statistics and build mathematically valid PCAP files with correct checksums, headers, and handshakes.

## Repository Structure

* `data/raw_pcaps/`: Baseline PCAPs of real gaming, streaming, and office work (Not tracked in Git).
* `data/processed_flows/`: Extracted time-series CSV data used for ML training.
* `models/`: Saved ML models (e.g., TimeGAN, LSTMs) and scaling parameters.
* `notebooks/`: Jupyter notebooks for data exploration and model testing.
* `src/config.py`: Central configuration for directory paths and file-to-profile mappings.
* `src/feature_extractor.py`: Parses raw PCAP files into ML-readable time-series data.
* `src/train.py`: Code to train the sequential machine learning models.
* `src/generator.py`: Uses the trained model to output artificial packet arrays and time delays.
* `src/pcap_crafter.py`: Scapy script that takes ML output and constructs valid `.pcap` files.

## Datasets and Acknowledgements

The data used to train the machine learning models in this project is sourced from two primary open-source datasets:

**1. Office and Streaming Data: UNB ISCX VPN-nonVPN Dataset (2016)**
> Gerard Drapper Gil, Arash Habibi Lashkari, Mohammad Mamun, Ali A. Ghorbani, "Characterization of Encrypted and VPN Traffic Using Time-Related Features", In Proceedings of the 2nd International Conference on Information Systems Security and Privacy(ICISSP 2016) , pages 407-414, Rome, Italy.

**2. Gaming Data: LORIA Cloud Gaming Dataset**
Provides high-fidelity captures of UDP-heavy gaming and interactive real-time traffic to train the gaming profile.

---

## Step-by-Step Execution Guide

### Step 1: Environment Setup
Clone the repository and set up a clean Python environment to avoid dependency conflicts.

```bash
git clone <your-repo-url>
cd synthetic-pcap-generator
python -m venv venv

# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```
### Step 2: Data Preparation
1. Download the ISCX and LORIA datasets.

2. Extract the ```.pcap``` or ```.pcapng``` files and place them inside the ```data/raw_pcaps/``` directory. You can keep them inside subfolders (e.g., ```data/raw_pcaps/NonVPN-PCAPs-01/```), as the extraction script searches recursively.

3. Open ```src/config.py``` and ensure the FILE_MAPPINGS dictionary correctly targets the substrings in your downloaded file names.

### Step 3: Feature Extraction
Translate the raw binary network captures into mathematical time-series data (packet sizes and inter-arrival times).
```python src/feature_extractor.py```

Expected Output: Creates ```working_processed.csv```, ```streaming_processed.csv```, and ```gaming_processed.csv``` inside ```data/processed_flows/```.

### Step 4: Model Training
Train the LSTM neural networks to learn the behavioral patterns of each profile.
python ```src/train.py```
(Note: You will need to edit the ```if __name__ == "__main__":``` block in the script to loop through all three profiles, or pass them via command line arguments).
Expected Output: Saves ```.h5``` model files and ```.pkl``` scaler files into the ```models/``` directory.

### Step 5: Synthetic Flow Generation
Use the trained models to generate completely new, artificial sequences of traffic metadata.

```python src/generator.py```
Expected Output: Creates synthetic_<mode>_flow.csv inside data/processed_flows/.

### Step 6: PCAP Crafting
Convert the generated synthetic metadata back into mathematically valid, Wireshark-readable ```.pcap``` files.

```python src/pcap_crafter.py```
Expected Output: Generates the final ```final_synthetic_<mode>.pcap``` files in the root directory of the project.