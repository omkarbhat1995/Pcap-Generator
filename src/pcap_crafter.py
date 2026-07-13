"""
src/pcap_crafter.py
Takes synthetic flow data (CSV) and writes mathematically valid .pcap files using Scapy.
"""
import time
import pandas as pd
from scapy.all import IP, TCP, wrpcap, Ether
from config import PROCESSED_FLOWS_DIR, PROJECT_ROOT

def craft_pcap(mode_label, src_ip="192.168.1.100", dst_ip="10.0.0.50"):
    """
    Reads synthetic packet sizes and inter-arrival times, then crafts a valid PCAP.
    """
    input_filename = f"synthetic_{mode_label}_flow.csv"
    input_path = PROCESSED_FLOWS_DIR / input_filename
    
    print(f"Loading synthetic data from: {input_path}")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}. Run generator.py first.")
        return

    packets = []
    
    # Base timestamp (use current time as the start of the capture)
    current_time = time.time()
    
    # TCP Sequence tracking
    seq_num = 1000
    ack_num = 1000

    print(f"Crafting {len(df)} packets for {mode_label} mode. This may take a moment...")
    
    for index, row in df.iterrows():
        packet_size = int(row['Packet_Size'])
        iat = float(row['IAT'])
        
        # 1. Calculate Timestamps
        # Advance the timestamp by the Inter-Arrival Time predicted by the ML model
        current_time += iat
        
        # 2. Build Base Headers
        # A standard Ethernet + IP + TCP header without payload is usually 54-66 bytes.
        # We'll use 54 bytes as our baseline (Ethernet: 14, IP: 20, TCP: 20).
        eth_layer = Ether()
        ip_layer = IP(src=src_ip, dst=dst_ip)
        tcp_layer = TCP(sport=50000, dport=443, seq=seq_num, ack=ack_num, flags="PA")
        
        # 3. Calculate Padding
        # The ML model tells us how big the *entire* packet should be.
        # We must pad the payload to ensure the final Scapy packet matches that size.
        base_size = len(eth_layer / ip_layer / tcp_layer)
        payload_size = max(0, packet_size - base_size)
        payload = b"X" * payload_size
        
        # 4. Construct Final Packet
        pkt = eth_layer / ip_layer / tcp_layer / payload
        
        # Force Scapy to assign the synthetic timestamp to the packet metadata
        pkt.time = current_time
        
        packets.append(pkt)
        
        # Increment sequence numbers realistically (simplified for this baseline)
        seq_num += payload_size if payload_size > 0 else 1

    # 5. Write to Disk
    output_filename = f"final_synthetic_{mode_label}.pcap"
    output_path = PROJECT_ROOT / output_filename
    
    print(f"Writing valid PCAP file with checksums...")
    wrpcap(str(output_path), packets)
    print(f"Success! Synthetic PCAP saved to: {output_path}")

if __name__ == "__main__":
    # Example usage: Craft the synthetic streaming PCAP
    # Ensure you have already run generator.py to create the CSV!
    craft_pcap(mode_label="streaming")