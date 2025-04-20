import os
import librosa
import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis

# === Settings ===
audio_root = "./audio_samples/Classical_Piano"
output_feature_csv = "audio_features.csv"
output_label_csv = "dataset_labels.csv"
output_classification_csv = "classification_labels.csv"

# === Label Mapping for classification ===
label_mapping = {
    "flat": 0,
    "low_boost": 1,
    "low_cut": 2,
    "mid_boost": 3,
    "mid_cut": 4,
    "high_boost": 5,
    "high_cut": 6,
}

# === Helper: Extract audio features ===
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=44100)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfccs[:3], axis=1)
    rms_energy = np.mean(librosa.feature.rms(y=y))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
    spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))
    return { #correlation分析
        "spectral_centroid": spectral_centroid,
        # "spectral_bandwidth": spectral_bandwidth, #有用前後那個
        "spectral_rolloff": spectral_rolloff,
        "mfcc_1": mfcc_mean[0],
        "mfcc_2": mfcc_mean[1],
        "mfcc_3": mfcc_mean[2],
        "mfcc_4": mfcc_mean[3],
        "mfcc_5": mfcc_mean[4],
        "mfcc_6": mfcc_mean[5],
        "mfcc_7": mfcc_mean[6],
        "mfcc_8": mfcc_mean[7],
        "mfcc_9": mfcc_mean[8],
        "mfcc_10": mfcc_mean[9],
        "mfcc_11": mfcc_mean[10],
        "mfcc_12": mfcc_mean[11],
        "mfcc_13": mfcc_mean[12],
        "rms_energy": rms_energy,
        # "zero_crossing_rate": zero_crossing_rate, 
        # "spectral_contrast": spectral_contrast,
        # "skewness": skew(y),
        # "kurtosis": kurtosis(y)
    }

# === Helper: Parse filename into EQ regression labels ===
def parse_eq_label(filename):
    label = {"EQ_300": 0, "EQ_600": 0, "EQ_1000": 0}
    name_parts = filename.lower().split("_")
    if "eq" in name_parts:
        try:
            idx = name_parts.index("eq")
            freq = name_parts[idx + 1]
            action = name_parts[idx + 2]
            if freq in ["300", "600", "1000"]:
                value = 8.6 if action == "boost" else -8.6
                label[f"EQ_{freq}"] = value
        except:
            pass  # fallback to all 0
    return label

# === Helper: Classify filename into 7-class label ===
def parse_class_label(filename):
    name = filename.lower()
    if "eq" not in name:
        return label_mapping["flat"]
    if "300" in name:
        return label_mapping["low_boost"] if "boost" in name else label_mapping["low_cut"]
    if "600" in name:
        return label_mapping["mid_boost"] if "boost" in name else label_mapping["mid_cut"]
    if "1000" in name:
        return label_mapping["high_boost"] if "boost" in name else label_mapping["high_cut"]
    return label_mapping["flat"]

# === Main Loop ===
feature_rows = []
label_rows = []
classification_rows = []

for root, _, files in os.walk(audio_root):
    for fname in files:
        if fname.endswith(".wav"):
            path = os.path.join(root, fname)
            print(f"Processing: {fname}")
            feats = extract_features(path)
            feats["file"] = fname
            feature_rows.append(feats)

            label = parse_eq_label(fname)
            label["file"] = fname
            label_rows.append(label)

            classification_label = {"label": parse_class_label(fname),"file": fname}
            classification_rows.append(classification_label)

# === Save to CSV ===
features_df = pd.DataFrame(feature_rows)
labels_df = pd.DataFrame(label_rows)
classification_df = pd.DataFrame(classification_rows)

features_df.to_csv(output_feature_csv, index=False)
labels_df.to_csv(output_label_csv, index=False)
classification_df.to_csv(output_classification_csv, index=False)

print("✅ All feature, regression, and classification CSV files generated!")