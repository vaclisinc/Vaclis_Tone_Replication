import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# === Step 1: Load Data ===
features_df = pd.read_csv("audio_features.csv")
labels_df = pd.read_csv("dataset_labels.csv")
merged_df = pd.merge(features_df, labels_df, on="file")

# === Step 2: Prepare Input (X) and Output (y) ===
X = merged_df.drop(columns=["file", "EQ_80", "EQ_240", "EQ_2500", "EQ_4000", "EQ_10000"]).values
y = merged_df[["EQ_80", "EQ_240", "EQ_2500", "EQ_4000", "EQ_10000"]].values

# Standardize features (跟 sklearn 一樣，記得只 fit on train)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === Step 3: PyTorch Dataset & DataLoader ===
class EQQDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

train_ds = EQQDataset(X_train_scaled, y_train)
test_ds  = EQQDataset(X_test_scaled,  y_test)
train_dl = DataLoader(train_ds, batch_size=64, shuffle=True)
test_dl  = DataLoader(test_ds, batch_size=256, shuffle=False)

# === Step 4: Define Model ===
class SimpleMLP(nn.Module):
    def __init__(self, in_dim, hidden=64, out_dim=5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim)
        )
    def forward(self, x):
        return self.net(x)

model = SimpleMLP(X_train_scaled.shape[1])

# === Step 5: Train ===
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()
epochs = 60

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for xb, yb in train_dl:
        pred = model(xb)
        loss = loss_fn(pred, yb)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * len(xb)
    print(f"Epoch {epoch+1}/{epochs} - Train MSE: {running_loss/len(train_ds):.4f}")

# === Step 6: Evaluation ===
model.eval()
with torch.no_grad():
    X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
    y_pred_tensor = model(X_test_tensor)
    y_pred = y_pred_tensor.numpy()

# MSE
mse = np.mean((y_pred - y_test)**2)
print(f"Test Mean Squared Error: {mse:.4f}")

# === Step 7: Plot ===
plt.figure(figsize=(12, 4))
label_list = ["EQ_80", "EQ_240", "EQ_2500", "EQ_4000", "EQ_10000"]
for i, label in enumerate(label_list):
    plt.subplot(1, 5, i+1)
    plt.scatter(y_test[:, i], y_pred[:, i], alpha=0.7)
    plt.plot([-12, 12], [-12, 12], color='r', linestyle='--')
    plt.xlabel("True")
    plt.ylabel("Predicted")
    plt.title(f"{label} NN Prediction")
plt.tight_layout()
plt.show()