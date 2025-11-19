'''
import pandas as pd

# Load the CSV files
file1 = "NSMES1988updated.csv"
file2 = "NSMES1988-NSMES1988.csv"

# Read both files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Step 1: Compare column headers
print("🔍 Comparing column headers...")
columns1 = df1.columns.tolist()
columns2 = df2.columns.tolist()

if columns1 == columns2:
    print("✅ Column headers are identical.")
else:
    print("❌ Column headers differ.")
    print("File 1 columns:", columns1)
    print("File 2 columns:", columns2)

# Step 2: Check for row count mismatch
print("\n🔍 Comparing row counts...")
if len(df1) == len(df2):
    print(f"✅ Both files have {len(df1)} rows.")
else:
    print(f"❌ Row count mismatch: File 1 has {len(df1)} rows, File 2 has {len(df2)} rows.")

# Step 3: Compare row-by-row and column-by-column
print("\n🔍 Checking for data misalignment or differences...")
differences = []

min_rows = min(len(df1), len(df2))
for i in range(min_rows):
    row1 = df1.iloc[i]
    row2 = df2.iloc[i]
    for col in set(columns1).intersection(columns2):
        val1 = row1[col]
        val2 = row2[col]
        if pd.isnull(val1) and pd.isnull(val2):
            continue
        if val1 != val2:
            differences.append((i, col, val1, val2))

if differences:
    print(f"❌ Found {len(differences)} differences:")
    for diff in differences[:10]:  # Show first 10 differences
        print(f"Row {diff[0]} | Column '{diff[1]}' | File1: {diff[2]} | File2: {diff[3]}")
    if len(differences) > 10:
        print("...and more. Consider exporting the differences for full review.")
else:
    print("✅ No data differences found in aligned rows.")

# Optional: Save differences to CSV
# pd.DataFrame(differences, columns=["Row", "Column", "File1_Value", "File2_Value"]).to_csv("differences.csv", index=False)
'''

import pandas as pd

# Load both CSVs
df_updated = pd.read_csv("NSMES1988updated.csv")
df_old = pd.read_csv("NSMES1988-NSMES1988.csv")

# Drop the index column from the old file if it exists
if 'Unnamed: 0' in df_old.columns:
    df_old = df_old.drop(columns=['Unnamed: 0'])

# Rescale 'income' and 'age' in the old file
df_old['income'] = df_old['income'] * 10000
df_old['age'] = df_old['age'] * 10

# Align both DataFrames to shared columns only
shared_columns = df_updated.columns.intersection(df_old.columns)
df_updated = df_updated[shared_columns]
df_old = df_old[shared_columns]

# Compare shapes
print("🔍 Shape comparison:")
print(f"Updated file shape: {df_updated.shape}")
print(f"Old file shape:     {df_old.shape}")

# Compare data
print("\n🔍 Comparing data...")
differences = (df_updated != df_old) & ~(df_updated.isnull() & df_old.isnull())

if differences.any().any():
    diff_locs = differences.stack()[differences.stack()].index.tolist()
    print(f"❌ Found {len(diff_locs)} differences.")
    for i, (row, col) in enumerate(diff_locs[:10]):
        val1 = df_updated.at[row, col]
        val2 = df_old.at[row, col]
        print(f"Row {row} | Column '{col}' | Updated: {val1} | Old: {val2}")
    if len(diff_locs) > 10:
        print("...and more. Consider exporting the full list.")
else:
    print("✅ All values match after adjustments.")

