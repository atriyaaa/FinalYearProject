# import pandas as pd

# df = pd.read_csv("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv")
# unique_subtypes = df["subtype"].unique()

# print("Total subtypes:", len(unique_subtypes))
# print("Subtype examples:", unique_subtypes[:10])

# import pandas as pd

# # Change this path to match where your dataset is
# df = pd.read_csv("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv")

# print("✅ Subtype frequency distribution:")
# print(df["subtype"].value_counts())

# df = pd.read_csv("datasets/final_clean_merged.csv")
# print(df[df["subtype"].str.contains("BRCA", na=False)]["subtype"].value_counts())

# import pandas as pd

# df = pd.read_csv("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv")
# print("✅ Subtype counts:")
# print(df["subtype"].value_counts())

# import joblib

# enc = joblib.load("cancer_classification_project/models/label_encoders.pkl")["subtype"]
# print(enc.classes_)

import joblib

enc = joblib.load("cancer_classification_project/models/label_encoders.pkl")["subtype"]
print("📊 Classes in encoder:")
for i, label in enumerate(enc.classes_):
    print(f"{i}: {label}")
