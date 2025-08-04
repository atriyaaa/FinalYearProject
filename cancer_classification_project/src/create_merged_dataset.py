import pandas as pd
import os

# Paths to merged files
merged_files = [
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/merged/merged_breast.csv",
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/merged/merged_colorectal.csv",
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/merged/merged_kidney.csv",
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/merged/merged_lung.csv",
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/merged/merged_prostate.csv"
]

# Column renaming/dropping for standardization
COLUMN_FIXES = {
    "breast": {
        "age_at_diagnosis": "age",
        "gender": "sex"
    },
    "colorectal": {},
    "kidney": {
        "age_at_diagnosis": "age",
        "gender": "sex"
    },
    "lung": {},
    "prostate": {
        "tumor disease anatomic site": None,
        "vital status": "vital_status"
    }
}

ESSENTIAL_CLINICAL = ["barcode", "subtype", "age", "sex", "vital_status"]
OPTIONAL = ["tumor_stage"]

cleaned_dfs = []

for path in merged_files:
    cancer_type = os.path.basename(path).replace("merged_", "").replace(".csv", "")
    print(f"\n📂 Processing: {cancer_type}")

    df = pd.read_csv(path)

    # Rename or drop specified columns
    fix_map = COLUMN_FIXES.get(cancer_type, {})
    df = df.rename(columns={k: v for k, v in fix_map.items() if v is not None})
    for k, v in fix_map.items():
        if v is None and k in df.columns:
            df = df.drop(columns=[k])

    # ✅ Just use the 'subtype' column directly
    if "subtype" in df.columns:
        print(f"✅ Using 'subtype' column for {cancer_type}")
    else:
        print(f"❌ 'subtype' column missing in {cancer_type} — skipping this file")
        continue

    print(df["subtype"].value_counts(dropna=False).head(10))

    # Ensure all required clinical columns exist
    for col in ESSENTIAL_CLINICAL + OPTIONAL:
        if col not in df.columns:
            df[col] = pd.NA

    # Drop incomplete rows and duplicates
    df = df.dropna(subset=ESSENTIAL_CLINICAL)
    df = df.drop_duplicates(subset="barcode")

    cleaned_dfs.append(df)

# Combine all datasets
merged_final = pd.concat(cleaned_dfs, ignore_index=True)
merged_final = merged_final.drop_duplicates(subset="barcode")

# Save final merged file
output_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_merged.csv"
merged_final.to_csv(output_path, index=False)

print(f"\n✅ Final full dataset saved to: {output_path}")
print(f"🧬 Total samples: {len(merged_final)}, Columns: {len(merged_final.columns)}")
