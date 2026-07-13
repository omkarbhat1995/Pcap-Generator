"""
src/feature_extractor.py
Reads raw PCAP files and extracts time-series flow statistics.
"""
import os
import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP
from scapy.layers.inet import IP, TCP, UDP
from scapy.utils import wrpcap
from config import RAW_PCAP_DIR, PROCESSED_FLOWS_DIR

def extract_features(pcap_filename, mode_label):
    """
    Parses a PCAP file and extracts [Timestamp, Protocol, Packet_Size, Direction].
    """
    pcap_path = RAW_PCAP_DIR / pcap_filename
    print(f"Loading PCAP: {pcap_path} (This might take a minute for large files...)")
    
    try:
        packets = rdpcap(str(pcap_path))
    except FileNotFoundError:
        print(f"Error: Could not find {pcap_path}")
        return None

    flow_data = []
    
    # Optional: Grab the first IP to loosely determine "direction" (internal vs external)
    # For a more robust setup, you might want to specify the host IP in config.py
    first_ip = packets[0][IP].src if packets[0].haslayer(IP) else None

    print(f"Extracting features for mode: {mode_label}...")
    for pkt in packets:
        if IP in pkt:
            timestamp = float(pkt.time)
            packet_size = len(pkt)
            
            # Determine Protocol (TCP = 6, UDP = 17)
            protocol = 'Other'
            if TCP in pkt:
                protocol = 'TCP'
            elif UDP in pkt:
                protocol = 'UDP'
                
            # Determine Direction (1 for Outbound, 0 for Inbound)
            direction = 1 if pkt[IP].src == first_ip else 0
            
            flow_data.append([timestamp, protocol, packet_size, direction])

    # Convert to DataFrame
    df = pd.DataFrame(flow_data, columns=['Timestamp', 'Protocol', 'Packet_Size', 'Direction'])
    
    # Calculate Inter-Arrival Time (IAT)
    # This is crucial for ML models to learn the "rhythm" of the traffic
    df['IAT'] = df['Timestamp'].diff().fillna(0)
    
    # Save to processed directory
    output_filename = f"{mode_label}_processed.csv"
    output_path = PROCESSED_FLOWS_DIR / output_filename
    df.to_csv(output_path, index=False)
    
    print(f"Successfully extracted {len(df)} packets.")
    print(f"Saved extracted features to: {output_path}\n")
    return df

if __name__ == "__main__":
    # Example usage: 
    # Place a file named 'sample_gaming.pcap' in data/raw_pcaps/
    # extract_features("sample_gaming.pcap", "gaming")
    print("Feature extractor ready. Call extract_features() with your PCAP file.")