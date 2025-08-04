import pandas as pd
import requests
import time

# Input and output paths
input_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/prostate/tcga_prad_expression_matrix.csv"
output_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/prostate/tcga_prad_expression_matrix_with_barcodes.csv"

# Load gene expression matrix
df = pd.read_csv(input_path)

# Get UUIDs from column headers (excluding the gene ID column)
uuids = df.columns[1:]
print(f"🧬 Found {len(uuids)} UUIDs in the file")

# Prepare query to GDC API
def map_uuid_to_barcode(uuid_list):
    url = "https://api.gdc.cancer.gov/files"
    headers = {"Content-Type": "application/json"}
    payload = {
        "filters": {
            "op": "in",
            "content": {
                "field": "file_id",
                "value": uuid_list
            }
        },
        "fields": "file_id,associated_entities.entity_submitter_id",
        "format": "JSON",
        "size": len(uuid_list)
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    results = response.json()["data"]["hits"]

    return {
        item["file_id"]: item["associated_entities"][0]["entity_submitter_id"]
        for item in results if item["associated_entities"]
    }

# Map UUIDs to TCGA barcodes
uuid_to_barcode = map_uuid_to_barcode(list(uuids))

# Replace column names
new_columns = [df.columns[0]] + [uuid_to_barcode.get(col, col) for col in uuids]
df.columns = new_columns

# Save to CSV
df.to_csv(output_path, index=False)
print(f"✅ Saved updated file to: {output_path}")
