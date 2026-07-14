"""
src/feature_extractor.py
Reads directories of PCAP/PCAPNG files and extracts time-series flow statistics.
"""
import pandas as pd
from pathlib import Path
from scapy.all import rdpcap, IP, TCP, UDP
from config import RAW_PCAP_DIR, PROCESSED_FLOWS_DIR, FILE_MAPPINGS

def process_single_pcap(pcap_path):
    """Extracts features from a single PCAP file."""
    print(f"  -> Reading {pcap_path.name}...")
    try:
        packets = rdpcap(str(pcap_path))
    except Exception as e:
        print(f"  -> Error reading {pcap_path.name}: {e}")
        return []

    flow_data = []
    first_ip = packets[0][IP].src if packets[0].haslayer(IP) else None

    for pkt in packets:
        if IP in pkt:
            timestamp = float(pkt.time)
            packet_size = len(pkt)
            
            protocol = 'Other'
            if TCP in pkt:
                protocol = 'TCP'
            elif UDP in pkt:
                protocol = 'UDP'
                
            direction = 1 if pkt[IP].src == first_ip else 0
            flow_data.append([timestamp, protocol, packet_size, direction])
            
    return flow_data

def build_profile_dataset(mode_label):
    """Finds all mapped files for a mode, extracts data, and combines them."""
    if mode_label not in FILE_MAPPINGS:
        print(f"Error: Mode '{mode_label}' not defined in config.py")
        return

    target_substrings = FILE_MAPPINGS[mode_label]
    if not target_substrings:
        print(f"Skipping {mode_label}: No file mappings defined.")
        return

    print(f"\nBuilding dataset for profile: [{mode_label.upper()}]")
    
    # Recursively find all .pcap and .pcapng files in the raw_pcaps directory
    all_files = list(RAW_PCAP_DIR.rglob("*.pcap")) + list(RAW_PCAP_DIR.rglob("*.pcapng"))
    
    # Filter files that match this profile's substrings
    matched_files = []
    for f in all_files:
        filename_lower = f.name.lower()
        if any(sub.lower() in filename_lower for sub in target_substrings):
            matched_files.append(f)

    if not matched_files:
        print(f"No matching files found in {RAW_PCAP_DIR} for {mode_label}.")
        return

    print(f"Found {len(matched_files)} files for {mode_label}.")
    
    master_flow_data = []
    for file_path in matched_files:
        file_data = process_single_pcap(file_path)
        master_flow_data.extend(file_data)

    if not master_flow_data:
        print(f"Failed to extract any usable IP packets for {mode_label}.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(master_flow_data, columns=['Timestamp', 'Protocol', 'Packet_Size', 'Direction'])
    
    # Sort by timestamp globally (since we merged multiple files)
    df = df.sort_values(by='Timestamp').reset_index(drop=True)
    
    # Calculate Inter-Arrival Time (IAT)
    df['IAT'] = df['Timestamp'].diff().fillna(0)
    
    # Save to processed directory
    output_path = PROCESSED_FLOWS_DIR / f"{mode_label}_processed.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Successfully extracted {len(df)} total packets.")
    print(f"Saved combined profile to: {output_path}\n")

if __name__ == "__main__":
    # Process both available profiles
    build_profile_dataset("streaming")
    build_profile_dataset("working")