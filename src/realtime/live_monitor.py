"""
live_monitor.py (Final Version)
-----------------------------------------------------
Phase 4: Real-Time Intrusion Detection System (AI-NDS)

Description:
  • Continuously captures live packets using Scapy
  • Extracts minimal flow features
  • Aligns live data with model-trained feature schema
  • Classifies packets in real-time as Normal or Intrusion
-----------------------------------------------------
"""

import joblib
import pandas as pd
from scapy.all import sniff, IP
from datetime import datetime
import os

# 1. Load model & preprocessor

MODEL_PATH = "src/models/cic_ids2018_model.joblib"
SCALER_PATH = "src/models/cic_ids2018_preprocess.joblib"

print("🧠 Loading trained model and scaler...")
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
print("✅ Model and scaler loaded successfully.\n")

# The model was trained on these features:
trained_features = scaler.feature_names_in_

# 2. Setup log file

LOG_DIR = "data"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "realtime_log.csv")

if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "Timestamp", "Src IP", "Dst IP", "Protocol", 
        "Packet Length", "Prediction"
    ]).to_csv(LOG_FILE, index=False)

# 3. Packet → Feature extraction

def extract_features(packet):
    """Extract minimal features from live packets"""
    try:
        if IP in packet:
            return {
                "Src IP": packet[IP].src,
                "Dst IP": packet[IP].dst,
                "Protocol": packet[IP].proto,
                "Packet Length": len(packet),
                "Timestamp": datetime.now().timestamp(),
            }
    except Exception:
        pass
    return None


# 4. Real-time packet prediction

def classify_packet(packet):
    """Predict and log result for each captured packet"""
    features = extract_features(packet)
    if features is None:
        return

    df = pd.DataFrame([features])

    # 🧩 Align with model’s expected features
    for col in trained_features:
        if col not in df.columns:
            df[col] = 0  # fill missing ones
    for col in df.columns:
        if col not in trained_features:
            df.drop(col, axis=1, inplace=True, errors='ignore')

    # Ensure correct column order
    df = df[trained_features]

    try:
        X_scaled = scaler.transform(df.fillna(0))
        y_pred = model.predict(X_scaled)
        label = int(y_pred[0])

        result = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Src IP": features.get("Src IP", ""),
            "Dst IP": features.get("Dst IP", ""),
            "Protocol": features.get("Protocol", ""),
            "Packet Length": features.get("Packet Length", 0),
            "Prediction": "⚠️ Intrusion" if label == 1 else "✅ Normal"
        }

        # Print result
        if label == 1:
            print(f"[{result['Timestamp']}] ⚠️ Intrusion detected: {result['Src IP']} → {result['Dst IP']}")
        else:
            print(f"[{result['Timestamp']}] ✅ Normal: {result['Src IP']} → {result['Dst IP']}")

        # Log result
        pd.DataFrame([result]).to_csv(LOG_FILE, mode='a', header=False, index=False)

    except Exception as e:
        print("Error during prediction:", e)

# 5. Start live capture

print("🚀 Starting real-time network monitoring...")
print("Press Ctrl + C to stop.\n")

try:
    sniff(prn=classify_packet, store=0)
except KeyboardInterrupt:
    print("\n🛑 Monitoring stopped by user.")
    print(f"📁 Logs saved to: {LOG_FILE}")
