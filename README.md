# 🧠 AI-NDS – AI-Based Network Intrusion Detection System

> **A Real-Time Machine Learning Powered Network Intrusion Detection System (NIDS)**  
> Designed to analyze live network traffic, detect anomalies, and visualize results instantly  
> using Artificial Intelligence, Data Analytics, and Cybersecurity principles.

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
10. [Future Scope](#-future-scope)
11. [Author](#-author)
12. [License](#-license)

---

## 🌐 **Overview**

The **AI-NDS (Artificial Intelligence – Network Detection System)** is a **real-time cybersecurity project** built to automatically detect malicious or anomalous network activities.

It leverages **Machine Learning (Random Forest, XGBoost)** models trained on the **CIC-IDS-2018 dataset**, and integrates **real-time packet capture** with a **Streamlit-powered dashboard** for live monitoring, visualization, and alerting.

### 🎯 **Objectives**
- Detect network intrusions using AI-based classification.  
- Capture and process live packet data in real time.  
- Visualize and alert suspicious activity dynamically.  
- Provide a scalable, modular, and modern NIDS architecture.

---

## 🏗️ **Project Architecture**

```text
┌────────────┐     ┌────────────────────┐     ┌────────────────┐     ┌──────────────────┐
│  Packet    │     │  Feature Extraction│     │ Machine Learning│     │  Visualization   │
│  Capture   ├──▶──┤  & Preprocessing   ├──▶──┤ Model Inference │──▶──┤  Dashboard (UI) │
└────────────┘     └────────────────────┘     └────────────────┘     └──────────────────┘
        ↑                                                              │
        └───────────── Continuous Real-Time Monitoring ────────────────┘
⚙️ Implementation Phases
Phase	Description	Status
Phase 1 – Dataset Preparation	Collected, cleaned, and preprocessed CIC-IDS-2018 dataset.	✅ Completed
Phase 2 – Feature Engineering & Capture	Extracted real-time network traffic using Scapy/PyShark matching the training schema.	✅ Completed
Phase 3 – Model Training	Trained Random Forest achieving 99.9% accuracy; saved as .joblib.	✅ Completed
Phase 4 – Real-Time Detection	Captured live packets → Extracted features → Predicted normal/intrusion in real-time.	✅ Completed
Phase 5 – Visualization	Developed an advanced Streamlit dashboard with alerts, charts, and logs.	✅ Completed

🧰 Tech Stack
Category	Tools / Libraries
Programming Language	Python 3.11
Data Handling	Pandas, NumPy
Machine Learning	Scikit-learn, XGBoost
Networking	Scapy, PyShark
Visualization	Streamlit, Plotly
Serialization	Joblib
OS / Platform	Windows / Linux
Version Control	Git & GitHub

📁 Project Structure
bash
Copy code
AI-NDS/
│
├── data/
│   ├── cic_ids_2018.csv                 # Cleaned dataset
│   ├── sample_flow.csv                  # Packet capture output
│   └── realtime_log.csv                 # Log file for dashboard
│
├── models/
│   ├── cic_ids2018_model.joblib         # Trained ML model
│   └── cic_ids2018_preprocess.joblib    # Preprocessing pipeline
│
├── src/
│   ├── training/
│   │   └── train_model.py               # Training + evaluation script
│   │
│   ├── realtime/
│   │   ├── capture.py                   # Live packet sniffing
│   │   ├── infer.py                     # CSV prediction
│   │   └── live_monitor.py              # Continuous monitor
│   │
│   └── dashboard/
│       └── app.py                       # Streamlit visualization dashboard
│
├── requirements.txt
├── README.md
└── LICENSE
🛠️ Setup & Usage
1️⃣ Clone the repository
bash
Copy code
git clone https://github.com/Dakshish-Murthy/AI-NDS.git
cd AI-NDS
2️⃣ Create & activate a virtual environment
bash
Copy code
python -m venv .venv
.venv\Scripts\activate      # (Windows)
source .venv/bin/activate   # (Linux/Mac)
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Train the Model (Optional)
bash
Copy code
python src/training/train_model.py
5️⃣ Capture Network Packets
bash
Copy code
python src/realtime/capture.py
6️⃣ Run Real-Time Detection
bash
Copy code
python src/realtime/live_monitor.py
7️⃣ Launch Dashboard
bash
Copy code
streamlit run src/dashboard/app.py
📊 Dashboard Features
🧠 Real-Time AI Detection – Instantly classifies network packets.
📈 Traffic Visualizations – Pie & line charts for traffic trends.
🚨 Animated Intrusion Alerts – Blinking red alert bar with beep sound.
✅ Dismissable Alerts – One-click acknowledgment of detected threats.
🕒 Alert History Log – Chronological record of past intrusions.
🎨 Modern UI – Dark theme, live dot animation, responsive layout.
🔄 Auto Refresh – Updates automatically every few seconds.

📈 Model Performance
Metric	Result
Accuracy	99.89%
Precision	99.80%
Recall	99.83%
F1-Score	99.81%

Achieved using the CIC-IDS-2018 Dataset (processed 2.8M flows).

📸 Sample Outputs
💻 Live Console (Real-Time Monitor)
yaml
Copy code
[2025-11-12 15:10:23] ✅ Normal: 10.0.3.0 → 8.8.8.8
[2025-11-12 15:10:27] ⚠️ Intrusion: 10.0.3.0 → 172.64.41.3
🧾 Streamlit Dashboard
📊 Real-time charts (Normal vs Intrusion)

🚨 Animated alert with sound + dismiss button

🕓 Historical log of all alerts

💚 “No Intrusions Detected” success box when safe

🧩 System Workflow
Packet Capture: Sniffs live packets using Scapy.

Feature Extraction: Derives 80+ features per flow.

Model Inference: Uses trained Random Forest model for classification.

Result Logging: Writes detection output to realtime_log.csv.

Dashboard Visualization: Displays traffic stats, alerts, and charts in real-time.

🔬 Results Summary
Component	Description	Output
Dataset	CIC-IDS-2018	4.1M records processed
ML Model	Random Forest	High accuracy, low latency
Real-Time Monitor	Python (Scapy + PyShark)	0.2s per flow
Dashboard	Streamlit + Plotly	Fully responsive & live updates

🔮 Future Scope
🧩 Integration with Firewall or Router (auto-block malicious IPs)

☁️ Deployment on Cloud Platforms (AWS / IBM / Azure)

🤖 Upgrade to Deep Learning (LSTM/CNN) models

📡 Expand to detect Zero-Day Attacks using anomaly detection

🧾 Exportable alert logs + centralized monitoring server