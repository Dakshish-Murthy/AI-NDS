# AI-NIDS Real-Time Inference Script (CIC-IDS2018 Compatible)


import pandas as pd
import joblib
import sys
import os
import warnings

# Suppress sklearn version warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Model paths
MODEL_PATH = "src/models/cic_ids2018_model.joblib"
SCALER_PATH = "src/models/cic_ids2018_preprocess.joblib"

# Check model files
if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    print("❌ Model or scaler file not found. Make sure both are in src/models/.")
    sys.exit(1)

# Load model and scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def predict_from_csv(file_path):
    print(f"\n🔍 Analyzing file: {file_path}")

    if not os.path.exists(file_path):
        print("❌ File not found:", file_path)
        sys.exit(1)

    # Read CSV
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # Clean headers

    # Drop label or other unwanted columns if present
    for col in ["Label", "AttackType"]:
        if col in df.columns:
            df = df.drop(columns=[col])
            print(f"⚙️ Dropped column: {col}")

    # Keep only numeric columns
    df = df.select_dtypes(exclude=['object']).fillna(0)

    # Align features to match training columns
    expected_features = scaler.feature_names_in_

    missing_cols = [col for col in expected_features if col not in df.columns]
    extra_cols = [col for col in df.columns if col not in expected_features]

    # Add missing columns with zeros
    if missing_cols:
        print(f"⚠️ Adding {len(missing_cols)} missing columns (e.g. {missing_cols[:3]}...)")
        for col in missing_cols:
            df[col] = 0

    # Drop unexpected extra columns
    if extra_cols:
        print(f"⚠️ Dropping {len(extra_cols)} extra columns (e.g. {extra_cols[:3]}...)")
        df = df.drop(columns=extra_cols)

    # Reorder columns to match training
    df = df[expected_features]

    # Scale and predict
    X_scaled = scaler.transform(df)
    preds = model.predict(X_scaled)
    probs = model.predict_proba(X_scaled)[:, 1]

    # Combine results
    results = pd.DataFrame({
        "Prediction": preds,
        "Confidence": probs
    })

    print("\n✅ Prediction Summary:")
    print(results["Prediction"].value_counts())
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/realtime/infer.py <path_to_csv>")
    else:
        predict_from_csv(sys.argv[1])
