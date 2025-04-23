import pandas as pd

valid_steps = set([-12, -8, -4, 0, 4, 8, 12])

labels_df = pd.read_csv("dataset_labels.csv")

def is_seven_steps(row):
    return all(row[f"EQ_{freq}"] in valid_steps for freq in [80, 240, 2500, 4000, 10000])

seven_mask = labels_df.apply(is_seven_steps, axis=1)
group_A = labels_df[seven_mask]
group_B = labels_df[~seven_mask]

group_A.to_csv("labels_seven_steps.csv", index=False)
group_B.to_csv("labels_interpolation.csv", index=False)
print(f"七檔: {len(group_A)}，interpolation: {len(group_B)}")



features_df = pd.read_csv("audio_features.csv")

features_seven = features_df[features_df['file'].isin(group_A['file'])]
features_interp = features_df[features_df['file'].isin(group_B['file'])]

features_seven.to_csv("features_seven_steps.csv", index=False)
features_interp.to_csv("features_interpolation.csv", index=False)