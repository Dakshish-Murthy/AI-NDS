from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import time
from datetime import datetime

flows = {}

def process_packet(packet):
    """Aggregate packets into flow-level stats"""
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        proto = packet[IP].proto
        key = (src, dst, proto)

        pkt_len = len(packet)
        timestamp = time.time()

        if key not in flows:
            flows[key] = {
                "Src IP": src,
                "Dst IP": dst,
                "Protocol": proto,
                "Packets": 0,
                "Bytes": 0,
                "Start": timestamp,
            }

        flows[key]["Packets"] += 1
        flows[key]["Bytes"] += pkt_len
        flows[key]["End"] = timestamp

def capture_traffic(duration=30):
    """Capture live packets for the specified duration (seconds)"""
    print(f"🔍 Capturing live packets for {duration} seconds…")
    sniff(prn=process_packet, store=0, timeout=duration)

    records = []
    for (_, _, _), stats in flows.items():
        duration = stats["End"] - stats["Start"] if "End" in stats else 0
        records.append({
            "Src IP": stats["Src IP"],
            "Dst IP": stats["Dst IP"],
            "Protocol": stats["Protocol"],
            "Total Packets": stats["Packets"],
            "Total Bytes": stats["Bytes"],
            "Flow Duration": duration
        })

    df = pd.DataFrame(records)
    df.to_csv("data/sample_flow.csv", index=False)
    print(f"✅ Saved extracted features to data/sample_flow.csv ({len(df)} flows)")

if __name__ == "__main__":
    capture_traffic(30)  # capture for 30 seconds
