# 🧠 AI-NDS – AI-Based Network Intrusion Detection System

> **A Real-Time Artificial Intelligence Powered Network Intrusion Detection System (NIDS)**  
> Designed to analyze live network traffic, detect anomalies, and visualize results instantly  
> using Machine Learning, Data Analytics, Networking, and Cybersecurity principles.

---

## 📜 **Table of Contents**
1. [Overview](#-overview)
2. [Project Architecture](#-project-architecture)
3. [Implementation Phases](#-implementation-phases)
4. [Tech Stack](#-tech-stack)
5. [Project Structure](#-project-structure)
6. [Setup & Usage](#️-setup--usage)
7. [Dashboard Features](#-dashboard-features)
8. [Model Performance](#-model-performance)
9. [Sample Outputs](#-sample-outputs)
10. [System Workflow](#-system-workflow)
11. [Results Summary](#-results-summary)
12. [Future Scope](#-future-scope)
13. [Author](#-author)
14. [License](#-license)

---

## 🌐 **Overview**

The **AI-NDS (Artificial Intelligence – Network Detection System)** is a fully functional  
**real-time cybersecurity system** that automatically detects malicious or anomalous network activity.

It integrates:
- 🚀 **Machine Learning (Random Forest, XGBoost)**
- 🔍 **Real-time packet sniffing (Scapy/PyShark)**
- 📊 **A professional Streamlit dashboard**
- 🛡️ **Live intrusion alerting system**

### 🎯 **Project Goals**
- Detect intrusions (DoS, DDoS, infiltration, brute-force attacks).
- Capture and process live network packets.
- Match extracted features with CIC-IDS-2018 dataset schema.
- Provide real-time analytics using an interactive dashboard.

---

## 🏗️ **Project Architecture**

┌────────────┐ ┌────────────────────┐ ┌──────────────────┐ ┌────────────────────┐
│ Packet │ │ Feature Extraction │ │ ML Inference │ │ Streamlit │
│ Capture ├──▶──┤ & Preprocessing ├──▶──┤ (Random Forest) ├──▶───┤ Live Dashboard │
└────────────┘ └────────────────────┘ └──────────────────┘ └────────────────────┘
▲ │ │
└─────────── Continuous Real-Time Monitoring & Alerting ───────────────────┘

yaml
Copy code

---

## ⚙️ **Implementation Phases**

| Phase | Description | Status |
|------|-------------|--------|
| **Phase 1 – Dataset Preparation** | Cleaned & preprocessed CIC-IDS-2018 dataset | ✅ Completed |
| **Phase 2 – Feature Engineering** | Real-time packet feature extraction aligned with dataset schema | ✅ Completed |
| **Phase 3 – Model Training** | Random Forest & XGBoost (99.9% accuracy) | ✅ Completed |
| **Phase 4 – Real-Time Detection** | Live packet capture → feature extraction → prediction | ✅ Completed |
| **Phase 5 – Visualization** | Interactive Streamlit dashboard | ✅ Completed |

---

## 🧰 **Tech Stack**

| Category | Tools |
|----------|--------|
| Programming Language | Python 3.11 |
| Data Handling | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Networking | Scapy, PyShark |
| Visualization | Streamlit, Plotly |
| Serialization | Joblib |
| Platform | Windows / Linux |
| Version Control | Git & GitHub |

---

## 📁 **Project Structure**

AI-NDS/
│
├── data/
│ ├── cic_ids_2018.csv # Cleaned dataset
│ ├── sample_flow.csv # Output of packet capture
│ └── realtime_log.csv # Live alert logs for dashboard
│
├── models/
│ ├── cic_ids2018_model.joblib # Trained ML model
│ └── cic_ids2018_preprocess.joblib # Preprocessing pipeline
│
├── src/
│ ├── training/
│ │ └── train_model.py # Model training + evaluation
│ │
│ ├── realtime/
│ │ ├── capture.py # Live packet capture
│ │ ├── infer.py # Prediction from CSV
│ │ └── live_monitor.py # Real-time monitoring engine
│ │
│ └── dashboard/
│ └── app.py # Streamlit live dashboard
│
├── requirements.txt
├── README.md
└── LICENSE

yaml
Copy code

---

## 🛠️ **Setup & Usage**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Dakshish-Murthy/AI-NDS.git
cd AI-NDS
2️⃣ Create & Activate Virtual Environment
bash
Copy code
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ (Optional) Train the Model
bash
Copy code
python src/training/train_model.py
5️⃣ Capture Live Network Packets
bash
Copy code
python src/realtime/capture.py
6️⃣ Run Real-Time Monitoring
bash
Copy code
python src/realtime/live_monitor.py
7️⃣ Launch Interactive Dashboard
bash
Copy code
streamlit run src/dashboard/app.py
📊 Dashboard Features
🔴 Real-Time Intrusion Alerts
Blinking red alert bar

Warning sound notification

Dismiss button to acknowledge alerts

📈 Live Traffic Visualizations
Normal vs Intrusion pie chart

Traffic over time (line chart)

Auto-refresh every few seconds

🧾 Recent Activity Logs
Last processed packets

IP source/destination

Prediction label

Timestamp

🎨 Modern UI
Dark theme

Responsive layout

Clean typography

📈 Model Performance
Metric	Score
Accuracy	99.89%
Precision	99.80%
Recall	99.83%
F1-Score	99.81%

Achieved using CIC-IDS-2018 (2.8M preprocessed flows).

📸 Sample Outputs
💻 Real-Time Console
yaml
Copy code
[2025-11-12 15:10:23] ✅ Normal: 10.0.3.0 → 8.8.8.8
[2025-11-12 15:10:27] ⚠️ Intrusion: 10.0.3.0 → 172.64.41.3
🧾 Dashboard Visuals
Live pie & line charts

Alert popup

Traffic logs

🧩 System Workflow
Packet Capture
Sniffs packets using Scapy and PyShark.

Feature Extraction
Converts raw packets into meaningful features (packet length, flags, flows).

Model Inference
Predicts whether flow is Normal or Intrusion.

Logging
Writes all results to realtime_log.csv.

Dashboard
Streamlit reads the log and shows charts + alerts live.

🔬 Results Summary
Component	Description	Output
Dataset	CIC-IDS-2018	4.1M records processed
ML Model	Random Forest	99.9% accuracy
Real-Time Monitor	Scapy + PyShark	~0.2s latency
Dashboard	Streamlit + Plotly	Full live analytics

🔮 Future Scope
🔥 Auto-block malicious IPs via firewall integration

🌐 Deploy on cloud platforms (AWS / IBM / Azure)

🤖 Upgrade to deep learning (CNN/LSTM-based IDS)

📡 Zero-day attack detection

📁 Exportable PDF/CSV security reports

🛜 Multi-device distributed monitoring

