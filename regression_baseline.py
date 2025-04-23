import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# === Step 1: Load Data ===
features_df = pd.read_csv("audio_features.csv")
labels_df = pd.read_csv("dataset_labels.csv")

merged_df = pd.merge(features_df, labels_df, on="file")


# === Step 2: Prepare Input (X) and Output (y) ===
X = merged_df.drop(columns=["file", "EQ_80", "EQ_240", "EQ_2500", "EQ_4000", "EQ_10000"])
y = merged_df[["EQ_80", "EQ_240", "EQ_2500", "EQ_4000", "EQ_10000"]]

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Step 3: Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# === Step 4: Train Model ===
model = LinearRegression()
model.fit(X_train, y_train)

# === Step 5: Predict & Evaluate ===
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.4f}")


# === Step 6: Compare Predictions ===
pred_df = pd.DataFrame(y_pred, columns=["EQ_80_pred", "EQ_240_pred", "EQ_2500_pred", "EQ_4000_pred", "EQ_10000_pred"])
pred_df[["EQ_80_true", "EQ_240_true", "EQ_2500_true", "EQ_4000_true", "EQ_10000_true"]] = y_test.reset_index(drop=True)
print(pred_df.head())


# === Step 7: Plot ===
plt.figure(figsize=(12, 4))
for i, label in enumerate(["EQ_80", "EQ_240", "EQ_2500", "EQ_4000", "EQ_10000"]):
    plt.subplot(1, 5, i+1)
    plt.scatter(pred_df[f"{label}_true"], pred_df[f"{label}_pred"], alpha=0.7)
    plt.plot([-12, 12], [-12, 12], color='r', linestyle='--')
    plt.xlabel("True")
    plt.ylabel("Predicted")
    plt.title(f"{label} Prediction")
plt.tight_layout()
plt.show()
