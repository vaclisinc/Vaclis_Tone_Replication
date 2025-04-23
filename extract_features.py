import os
import pandas as pd
import librosa
import numpy as np

# === Settings ===
audio_root = "./audio_samples/reaper/processed"
output_label_csv = "dataset_labels.csv"
output_feature_csv = "audio_features.csv"

band_freqs = [80, 240, 2500, 4000, 10000]

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=44100)
    features = {}
    features["spectral_centroid"] = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    features["spectral_bandwidth"] = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    features["spectral_rolloff"] = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    for i in range(mfccs.shape[0]):
        features[f"mfcc_{i+1}"] = np.mean(mfccs[i])
    features["rms_energy"] = np.mean(librosa.feature.rms(y=y))
    # 可以加其他特徵（如 zcr, contrast...），不需要可先註解
    # features["zero_crossing_rate"] = np.mean(librosa.feature.zero_crossing_rate(y))
    return features

def parse_eq_label(filename):
    label = {f"EQ_{freq}": 0 for freq in band_freqs}
    name = filename.replace(".wav", "")
    for freq in band_freqs:
        freq_str = str(freq)
        if freq_str in name:
            # e.g. "bell1_240_+3" → 找 freq 字串出現後的 "_+3"
            parts = name.split("_")
            for idx, part in enumerate(parts):
                if part == freq_str and idx+1 < len(parts):
                    try:
                        db_val = float(parts[idx+1])
                        label[f"EQ_{freq}"] = db_val
                    except ValueError:
                        # 避免 +3 這種寫法有字串頭 "+"
                        try:
                            db_val = float(parts[idx+1].replace("+",""))
                            if "+" in parts[idx+1]: db_val = abs(db_val)
                            if "-" in parts[idx+1]: db_val = -abs(db_val)
                            label[f"EQ_{freq}"] = db_val
                        except:
                            label[f"EQ_{freq}"] = 0
    return label

# Main loop
feature_rows = []
for fname in sorted(os.listdir(audio_root)):
    if fname.endswith(".wav"):
        fpath = os.path.join(audio_root, fname)
        feats = extract_features(fpath)
        feats["file"] = fname
        feature_rows.append(feats)

features_df = pd.DataFrame(feature_rows)
features_df.to_csv(output_feature_csv, index=False)
print(f"✅ All features saved to {output_feature_csv}!")

label_rows = []
for fname in sorted(os.listdir(audio_root)):
    if fname.endswith(".wav"):
        label = parse_eq_label(fname)
        label["file"] = fname
        label_rows.append(label)

labels_df = pd.DataFrame(label_rows)
labels_df.to_csv(output_label_csv, index=False)
print(f"✅ All EQ labels saved to {output_label_csv}!")