import os

output_dir = "./audio_samples/reaper/processed/"
steps = [-12, -8, -4, 0, 4, 8, 12]
bands = ["loshelf", "bell1", "bell2", "bell3", "hishelf"]

from itertools import product
all_combos = list(product(steps, repeat=5))

existing_set = set()
for fname in os.listdir(output_dir):
    if not fname.endswith(".wav"):
        continue
    # filename: 01_eq_loshelf_-8_bell1_4_bell2_12_bell3_0_hishelf_4.wav
    parts = fname.replace(".wav","").split("_")
    try:
        vals = []
        for b in bands:
            idx = parts.index(b)
            val = int(parts[idx + 1])
            vals.append(val)
        existing_set.add(tuple(vals))
    except Exception as e:
        print(f"Skip {fname} due to parsing error: {e}")

print(f"already finished amount of dataset：{len(existing_set)}")
print(f"haven't finished amount of dataset：{len(all_combos) - len(existing_set)}")

# If you want to test how many files you have done later on, comment below lines! ==========================

remaining_combos = [combo for combo in all_combos if combo not in existing_set]

# Seperate haven't finished amount of dataset, each batch 1000 possibility
batches = [remaining_combos[i:i+1000] for i in range(0, len(remaining_combos), 1000)]


remaining_combos = [combo for combo in all_combos if combo not in existing_set]
batches = [remaining_combos[i:i+1000] for i in range(0, len(remaining_combos), 1000)]

for idx, batch in enumerate(batches):
    with open(f"batch_{idx+1:02d}.lua", "w") as f:
        f.write("local combos = {\n")
        for c in batch:
            f.write(f"    {{{c[0]}, {c[1]}, {c[2]}, {c[3]}, {c[4]}}},\n")
        f.write("}\nreturn combos\n")