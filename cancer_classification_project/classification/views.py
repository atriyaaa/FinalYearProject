
# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
# import pandas as pd
# import joblib
# import os
# import traceback

# # === Load model artifacts ===
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "models")

# model = joblib.load(os.path.join(MODEL_DIR, "best_model.pkl"))
# scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
# pca = joblib.load(os.path.join(MODEL_DIR, "pca.pkl"))
# label_encoders = joblib.load(os.path.join(MODEL_DIR, "label_encoders.pkl"))

# # === Mapping subtype to cancer type ===
# SUBTYPE_TO_CANCER = {
#     "BRCA_LumA": "Breast",
#     "BRCA_LumB": "Breast",
#     "BRCA_Her2": "Breast",
#     "BRCA_Basal": "Breast",
#     "BRCA_Normal": "Breast",
#     "LUAD": "Lung",
#     "LUSC": "Lung",
#     "Clear Cell": "Kidney",
#     "Papillary": "Kidney",
#     "Chromophobe": "Kidney",
#     "Prostate Adenocarcinoma, Acinar Type": "Prostate",
#     "Prostate Adenocarcinoma, Other Subtype": "Prostate",
#     "STAGE I": "Colorectal",
#     "STAGE II": "Colorectal",
#     "STAGE III": "Colorectal",
#     "STAGE IV": "Colorectal",
#     "STAGE IA": "Colorectal",
#     "STAGE IB": "Colorectal",
#     "STAGE IIA": "Colorectal",
#     "STAGE IIB": "Colorectal",
#     "STAGE IIC": "Colorectal",
#     "STAGE IIIA": "Colorectal",
#     "STAGE IIIB": "Colorectal",
#     "STAGE IIIC": "Colorectal",
#     "STAGE IVA": "Colorectal",
#     "STAGE IVB": "Colorectal",
# }

# # === Load number-to-subtype mapping ===
# classes = label_encoders["subtype"].classes_
# number_to_subtype = {i: str(cls) for i, cls in enumerate(classes)}

# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def predict_csv(request):
#     try:
#         file = request.FILES.get('file')
#         if not file:
#             return Response({"error": "No file uploaded"}, status=400)

#         df = pd.read_csv(file)
#         print(f"Uploaded file shape: {df.shape}")

#         # === Align features ===
#         if hasattr(scaler, 'feature_names_in_'):
#             expected_features = list(scaler.feature_names_in_)
#             df = df.reindex(columns=expected_features, fill_value=0.0)

#         # === Scale + PCA + Predict ===
#         print("Scaling data...")
#         scaled = scaler.transform(df)
#         print("Reducing dimensions with PCA...")
#         reduced = pca.transform(scaled)

#         print("Running prediction...")
#         preds = model.predict(reduced)
#         print("Prediction complete.")
#         print("Raw predictions:", preds)

#         # Decode subtypes
#         decoded_subtypes = [number_to_subtype.get(int(p), f"Unknown ({p})") for p in preds]

#         # Map subtype → cancer type
#         cancer_types = [SUBTYPE_TO_CANCER.get(subtype, "Unknown") for subtype in decoded_subtypes]

#         # Prepare final result
#         results = [
#             {"sample": i + 1, "subtype": decoded_subtypes[i], "cancer_type": cancer_types[i]}
#             for i in range(len(decoded_subtypes))
#         ]

#         return Response({"predictions": results})

#     except Exception as e:
#         print("Error during prediction:", str(e))
#         traceback.print_exc()
#         return Response({"error": str(e)}, status=500)

# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
# from django.http import FileResponse, Http404
# import pandas as pd
# import joblib
# import os
# import shap
# import matplotlib.pyplot as plt
# import uuid
# import zipfile
# import traceback

# # === Load model artifacts ===
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "models")
# MEDIA_DIR = os.path.join(BASE_DIR, "media", "shap")
# os.makedirs(MEDIA_DIR, exist_ok=True)

# model = joblib.load(os.path.join(MODEL_DIR, "best_model.pkl"))
# scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
# pca = joblib.load(os.path.join(MODEL_DIR, "pca.pkl"))
# label_encoders = joblib.load(os.path.join(MODEL_DIR, "label_encoders.pkl"))

# # === Mapping subtype to cancer type ===
# SUBTYPE_TO_CANCER = {
#     "BRCA_LumA": "Breast",
#     "BRCA_LumB": "Breast",
#     "BRCA_Her2": "Breast",
#     "BRCA_Basal": "Breast",
#     "BRCA_Normal": "Breast",
#     "LUAD": "Lung",
#     "LUSC": "Lung",
#     "Clear Cell": "Kidney",
#     "Papillary": "Kidney",
#     "Chromophobe": "Kidney",
#     "Prostate Adenocarcinoma, Acinar Type": "Prostate",
#     "Prostate Adenocarcinoma, Other Subtype": "Prostate",
#     "STAGE I": "Colorectal",
#     "STAGE II": "Colorectal",
#     "STAGE III": "Colorectal",
#     "STAGE IV": "Colorectal",
#     "STAGE IA": "Colorectal",
#     "STAGE IB": "Colorectal",
#     "STAGE IIA": "Colorectal",
#     "STAGE IIB": "Colorectal",
#     "STAGE IIC": "Colorectal",
#     "STAGE IIIA": "Colorectal",
#     "STAGE IIIB": "Colorectal",
#     "STAGE IIIC": "Colorectal",
#     "STAGE IVA": "Colorectal",
#     "STAGE IVB": "Colorectal",
# }

# classes = label_encoders["subtype"].classes_
# number_to_subtype = {i: str(cls) for i, cls in enumerate(classes)}

# shap_plot_map = {}

# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def predict_csv(request):
#     try:
#         file = request.FILES.get('file')
#         if not file:
#             return Response({"error": "No file uploaded"}, status=400)

#         df = pd.read_csv(file)
#         if hasattr(scaler, 'feature_names_in_'):
#             expected_features = list(scaler.feature_names_in_)
#             df = df.reindex(columns=expected_features, fill_value=0.0)

#         scaled = scaler.transform(df)
#         reduced = pca.transform(scaled)
#         preds = model.predict(reduced)

#         decoded_subtypes = [number_to_subtype.get(int(p), f"Unknown ({p})") for p in preds]
#         cancer_types = [SUBTYPE_TO_CANCER.get(subtype, "Unknown") for subtype in decoded_subtypes]

#         explainer = shap.Explainer(model)
#         shap_values = explainer(reduced)

#         results = []
#         for i in range(len(reduced)):
#             sample_id = str(i + 1)
#             filename = f"shap_sample_{sample_id}.png"
#             path = os.path.join(MEDIA_DIR, filename)
#             shap.plots.bar(shap_values[i], show=False)
#             plt.savefig(path, bbox_inches='tight')
#             plt.close()
#             shap_plot_map[sample_id] = path

#             results.append({
#                 "sample": sample_id,
#                 "subtype": decoded_subtypes[i],
#                 "cancer_type": cancer_types[i],
#                 "shap_plot_url": f"/media/shap/{filename}"
#             })

#         return Response({"predictions": results})

#     except Exception as e:
#         traceback.print_exc()
#         return Response({"error": str(e)}, status=500)


# @api_view(['GET'])
# def get_shap_plot(request, sample_id):
#     try:
#         path = shap_plot_map.get(sample_id)
#         if path and os.path.exists(path):
#             return FileResponse(open(path, 'rb'), content_type='image/png')
#         raise Http404("SHAP plot not found")
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)


# @api_view(['GET'])
# def download_all_shap_plots(request):
#     try:
#         zip_path = os.path.join(MEDIA_DIR, "shap_plots_bundle.zip")
#         with zipfile.ZipFile(zip_path, 'w') as zipf:
#             for filename in os.listdir(MEDIA_DIR):
#                 if filename.endswith(".png"):
#                     zipf.write(os.path.join(MEDIA_DIR, filename), arcname=filename)

#         return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename="shap_plots_bundle.zip")
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)

import matplotlib
matplotlib.use('Agg')  # Must be before importing pyplot
import matplotlib.pyplot as plt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.http import FileResponse, Http404, JsonResponse
import pandas as pd
import joblib
import os
import shap
import zipfile
import traceback
import shutil
from datetime import datetime
import numpy as np
import warnings
import io
import base64
from django.urls import path


# Suppress sklearn warnings
warnings.filterwarnings("ignore", category=UserWarning)

# === Load model artifacts ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MEDIA_DIR = os.path.join(BASE_DIR, "media", "shap")
os.makedirs(MEDIA_DIR, exist_ok=True)

# Load models and label encoders
try:
    model = joblib.load(os.path.join(MODEL_DIR, "best_model.pkl"))
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    pca = joblib.load(os.path.join(MODEL_DIR, "pca.pkl"))
    label_encoders = joblib.load(os.path.join(MODEL_DIR, "label_encoders.pkl"))
except Exception as e:
    print(f"Error loading model artifacts: {str(e)}")
    # We'll handle this gracefully when the API is called

# === Mapping configurations ===
SUBTYPE_TO_CANCER = {
    "BRCA_LumA": "Breast",
    "BRCA_LumB": "Breast",
    "BRCA_Her2": "Breast",
    "BRCA_Basal": "Breast",
    "BRCA_Normal": "Breast",
    "LUAD": "Lung",
    "LUSC": "Lung",
    "Clear Cell": "Kidney",
    "Papillary": "Kidney",
    "Chromophobe": "Kidney",
    "Prostate Adenocarcinoma, Acinar Type": "Prostate",
    "Prostate Adenocarcinoma, Other Subtype": "Prostate",
    "STAGE I": "Colorectal",
    "STAGE II": "Colorectal",
    "STAGE III": "Colorectal",
    "STAGE IV": "Colorectal",
    "STAGE IA": "Colorectal",
    "STAGE IB": "Colorectal",
    "STAGE IIA": "Colorectal",
    "STAGE IIB": "Colorectal",
    "STAGE IIC": "Colorectal",
    "STAGE IIIA": "Colorectal",
    "STAGE IIIB": "Colorectal",
    "STAGE IIIC": "Colorectal",
    "STAGE IVA": "Colorectal",
    "STAGE IVB": "Colorectal",
}

# Global dictionary to store SHAP values and metadata
shap_data_store = {}

def initialize_classes():
    """Initialize class mapping from label encoders"""
    global number_to_subtype
    try:
        classes = label_encoders["subtype"].classes_
        number_to_subtype = {i: str(cls) for i, cls in enumerate(classes)}
    except (KeyError, AttributeError) as e:
        print(f"Error initializing classes: {str(e)}")
        number_to_subtype = {}

# Initialize classes
initialize_classes()

def clean_shap_directory():
    """Remove all files from the SHAP directory before generating new ones"""
    if os.path.exists(MEDIA_DIR):
        for filename in os.listdir(MEDIA_DIR):
            if filename.endswith('.png') or filename.endswith('.zip'):
                file_path = os.path.join(MEDIA_DIR, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

def generate_shap_plot(shap_values, feature_names, sample_idx, output_path):
    """
    Generate a horizontal SHAP bar plot for a single sample.
    
    Parameters:
    -----------
    shap_values : numpy.ndarray
        The SHAP values array. For a 3D array with shape (samples, classes, features),
        we'll extract the appropriate sample.
    feature_names : list
        Names of features corresponding to the last dimension of shap_values
    sample_idx : int
        Index of the sample to plot
    output_path : str
        Path to save the output plot
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import traceback
        
        print(f"Original SHAP values shape: {shap_values.shape}")
        
        # Extract the correct sample based on shape
        if len(shap_values.shape) == 3:  # (samples, classes, features)
            # For multi-class, we need to select one class (using the first class for now)
            # You might want to make this a parameter
            class_idx = 0
            shap_values_sample = shap_values[sample_idx, class_idx, :]
            print(f"Extracted sample shape: {shap_values_sample.shape}")
        elif len(shap_values.shape) == 2:  # (samples, features)
            shap_values_sample = shap_values[sample_idx, :]
            print(f"Extracted sample shape: {shap_values_sample.shape}")
        else:
            # If already a 1D array for a single sample
            shap_values_sample = shap_values
            print(f"Using provided sample shape: {shap_values_sample.shape}")
            
        plt.figure(figsize=(10, 6))
        
        # Ensure we have feature names for all features
        if feature_names is None or len(feature_names) == 0:
            feature_names = [f"Feature {i}" for i in range(len(shap_values_sample))]
        
        # Ensure feature names match SHAP vector length
        feature_count = len(shap_values_sample)
        if len(feature_names) != feature_count:
            if len(feature_names) > feature_count:
                feature_names = feature_names[:feature_count]
            else:
                feature_names += [f"Feature {i}" for i in range(len(feature_names), feature_count)]
        
        # Calculate feature importance
        importance = np.abs(shap_values_sample)
        
        # Get only available top features (max 20 or fewer)
        top_k = min(feature_count, 20)
        
        # Get indices of top k features by importance
        top_indices = importance.argsort()[-top_k:]
        
        # Debugging
        print(f"Top indices range: {min(top_indices)} to {max(top_indices)}")
        print(f"Feature count: {feature_count}")
        
        # Retrieve values and feature names for top features
        top_values = shap_values_sample[top_indices]
        top_names = [feature_names[i] for i in top_indices]
        
        # Create the plot
        colors = ['#ff0051' if val > 0 else '#008bfb' for val in top_values]
        y_pos = np.arange(len(top_names))
        
        plt.barh(y_pos, top_values, color=colors)
        plt.yticks(y_pos, top_names)
        plt.xlabel('SHAP Value (Impact on Prediction)')
        plt.title(f"SHAP Values for Sample {sample_idx + 1}")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
        
        return True
    except Exception as e:
        print(f"[SHAP Plot ERROR] {str(e)}")
        traceback.print_exc()
        
        plt.figure(figsize=(10, 6))
        plt.title(f"SHAP Values for Sample {sample_idx + 1}")
        plt.text(0.5, 0.5, f"Could not generate SHAP plot: {str(e)}", ha='center', va='center')
        plt.savefig(output_path)
        plt.close()
        
        return False
# def generate_shap_plot(shap_values, feature_names, sample_idx, output_path):
#     """Generate SHAP bar plot for a single sample"""
#     plt.figure(figsize=(10, 6))

#     try:
#         # Determine if it's a multi-class output
#         if isinstance(shap_values, list):
#             # Pick SHAP values for the predicted class (or just class 0)
#             shap_values_sample = shap_values[0][sample_idx]  # 2D array: [samples, features]
#         else:
#             shap_values_sample = shap_values[sample_idx]

#         # Fallback feature names
#         if feature_names is None or len(feature_names) == 0:
#             feature_names = [f"Feature {i}" for i in range(len(shap_values_sample))]

#         if len(feature_names) != len(shap_values_sample):
#             feature_names = feature_names[:len(shap_values_sample)]
#             if len(feature_names) < len(shap_values_sample):
#                 feature_names += [f"Feature {i}" for i in range(len(feature_names), len(shap_values_sample))]

#         # Ensure shap_values_sample is flat and scalar
#         if isinstance(shap_values_sample, np.ndarray):
#             # If values are multidimensional, flatten them by taking first dimension or summing
#             if shap_values_sample.ndim > 1:
#                 print(f"Debug: Found multidimensional SHAP values with shape {shap_values_sample.shape}")
#                 # Try to extract meaningful values - use first column if possible
#                 if shap_values_sample.shape[1] > 0:
#                     shap_values_sample = shap_values_sample[:, 0]
#                 else:
#                     # If no good approach, take the sum across dimensions
#                     shap_values_sample = np.sum(shap_values_sample, axis=1)

#         # Top 20 important features
#         # Calculate importance and sort
#         importance = np.abs(shap_values_sample)
#         top_indices = np.argsort(importance)[-20:]

#         # Extract scalar values for plotting
#         top_values = []
#         top_names = []
        
#         for i in top_indices:
#             idx = int(i) if not isinstance(i, (np.ndarray, list)) else int(i[0])
#             val = shap_values_sample[idx]
            
#             # Convert array values to scalars
#             if isinstance(val, np.ndarray):
#                 if val.size == 1:
#                     val = val.item()  # Extract scalar value
#                 else:
#                     # Handle multi-value array - take first element or sum
#                     val = val[0] if val.size > 0 else np.sum(val)
            
#             top_values.append(val)
#             top_names.append(feature_names[idx])

#         # Colors based on scalar values
#         colors = ['#ff0051' if val > 0 else '#008bfb' for val in top_values]
#         y_pos = np.arange(len(top_names))

#         plt.barh(y_pos, top_values, color=colors)
#         plt.yticks(y_pos, top_names)
#         plt.xlabel('SHAP Value (Impact on Prediction)')
#         plt.title(f"SHAP Values for Sample {sample_idx + 1}")
#         plt.tight_layout()
#         plt.savefig(output_path, dpi=150)
#         plt.close()
#         return True

#     except Exception as e:
#         print(f"[SHAP Plot ERROR] {str(e)}")
#         traceback.print_exc()
#         # Fallback plot
#         plt.figure(figsize=(10, 6))  # Create a new figure if necessary
#         plt.title(f"SHAP Values for Sample {sample_idx + 1}")
#         plt.text(0.5, 0.5, f"Could not generate SHAP plot: {str(e)}", ha='center', va='center')
#         plt.savefig(output_path)
#         plt.close()
#         return False


@api_view(['POST'])
@parser_classes([MultiPartParser])
def predict_csv(request):
    """Handle CSV upload, generate predictions and SHAP plots"""
    try:
        clean_shap_directory()
        # Clear the global SHAP data store
        global shap_data_store
        shap_data_store = {}
        
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        # Read CSV file
        try:
            df = pd.read_csv(file)
            if df.empty:
                return Response({"error": "Uploaded CSV file is empty"}, status=400)
        except Exception as e:
            return Response({"error": f"Error reading CSV file: {str(e)}"}, status=400)

        # Save original feature names
        original_feature_names = df.columns.tolist()

        # Ensure we have all expected features for the scaler
        if hasattr(scaler, 'feature_names_in_'):
            expected_features = list(scaler.feature_names_in_)
            missing_features = [f for f in expected_features if f not in df.columns]
            extra_features = [f for f in df.columns if f not in expected_features]
            
            if missing_features:
                print(f"Warning: Missing features in input data: {missing_features}")
                
            # Reindex to match expected features
            df = df.reindex(columns=expected_features, fill_value=0.0)
        
        # Transform data
        df_values = df.values
        scaled = scaler.transform(df_values)
        reduced = pca.transform(scaled)

        # Make predictions
        preds = model.predict(reduced)
        decoded_subtypes = [number_to_subtype.get(int(p), f"Unknown ({p})") for p in preds]
        cancer_types = [SUBTYPE_TO_CANCER.get(subtype, "Unknown") for subtype in decoded_subtypes]

        # Generate SHAP values
        try:
            # Use a simpler approach for SHAP visualization
            if hasattr(model, 'predict_proba'):
                # For classifiers, use a simpler direct approach
                def model_predict(x):
                    return model.predict_proba(x)
                explainer = shap.KernelExplainer(model_predict, reduced[:min(10, len(reduced))])
                shap_values = explainer.shap_values(reduced)
            else:
                # For regression or other models
                def model_predict(x):
                    return model.predict(x)
                explainer = shap.KernelExplainer(model_predict, reduced[:min(10, len(reduced))])
                shap_values = explainer.shap_values(reduced)
                
            print(f"SHAP values type: {type(shap_values)}")
            if isinstance(shap_values, list):
                print(f"List length: {len(shap_values)}")
                print(f"First element shape: {shap_values[0].shape}")
            else:
                print(f"SHAP values shape: {shap_values.shape}")
        except Exception as e:
            print(f"Error creating SHAP explainer: {str(e)}")
            traceback.print_exc()
            # Continue without SHAP values
            shap_values = None

        # Generate results
        results = []
        for i in range(len(reduced)):
            sample_id = str(i + 1)
            filename = f"shap_sample_{sample_id}.png"
            path = os.path.join(MEDIA_DIR, filename)
            
            shap_plot_success = False
            if shap_values is not None:
                try:
                    shap_plot_success = generate_shap_plot(shap_values, original_feature_names, i, path)
                except Exception as e:
                    print(f"Error generating SHAP plot for sample {sample_id}: {str(e)}")
                    traceback.print_exc()
            
            if shap_plot_success:
                # Store path for retrieval
                shap_data_store[sample_id] = {
                    'path': path,
                    'subtype': decoded_subtypes[i],
                    'cancer_type': cancer_types[i]
                }
                shap_url = f"/media/shap/{filename}"

                # shap_url = f"/api/get_shap_plot/{sample_id}/"
            else:
                shap_url = None

            results.append({
                "sample": sample_id,
                "subtype": decoded_subtypes[i],
                "cancer_type": cancer_types[i],
                "shap_plot_url": shap_url
            })

        return Response({"predictions": results})

    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_shap_plot(request, sample_id):
    """Serve a single SHAP plot image"""
    try:
        sample_data = shap_data_store.get(sample_id)
        if not sample_data or not os.path.exists(sample_data['path']):
            # If not found in memory, try to find the file directly
            fallback_path = os.path.join(MEDIA_DIR, f"shap_sample_{sample_id}.png")
            if os.path.exists(fallback_path):
                response = FileResponse(open(fallback_path, 'rb'), content_type='image/png')
                response['Content-Disposition'] = f'inline; filename="shap_plot_sample_{sample_id}.png"'
                return response
            else:
                return Response({"error": "SHAP plot not found"}, status=404)
        
        # Serve the file
        response = FileResponse(open(sample_data['path'], 'rb'), content_type='image/png')
        # Use 'inline' instead of 'attachment' to display in browser
        response['Content-Disposition'] = f'inline; filename="shap_plot_sample_{sample_id}.png"'
        return response
    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)


# @api_view(['GET'])
# @csrf_exempt
# @xframe_options_exempt
# def get_shap_plot(request, sample_id):
#     """Serve a single SHAP plot image for embedding"""
#     try:
#         sample_data = shap_data_store.get(sample_id)
#         if not sample_data or not os.path.exists(sample_data['path']):
#             # Try fallback path
#             fallback_path = os.path.join(MEDIA_DIR, f"shap_sample_{sample_id}.png")
#             if os.path.exists(fallback_path):
#                 response = FileResponse(open(fallback_path, 'rb'), content_type='image/png')
#                 response['Content-Disposition'] = f'inline; filename="shap_plot_sample_{sample_id}.png"'
#                 response["Access-Control-Allow-Origin"] = "*"
#                 return response
#             else:
#                 return Response({"error": "SHAP plot not found"}, status=404)

#         response = FileResponse(open(sample_data['path'], 'rb'), content_type='image/png')
#         response['Content-Disposition'] = f'inline; filename="shap_plot_sample_{sample_id}.png"'
#         response["Access-Control-Allow-Origin"] = "*"
#         return response
#     except Exception as e:
#         traceback.print_exc()
#         return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def download_all_shap_plots(request):
    """Create and serve a zip bundle of all SHAP plots"""
    try:
        if not os.path.exists(MEDIA_DIR) or not any(f.endswith('.png') for f in os.listdir(MEDIA_DIR)):
            return Response({"error": "No SHAP plots available"}, status=404)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"shap_plots_{timestamp}.zip"
        zip_path = os.path.join(MEDIA_DIR, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(MEDIA_DIR):
                if filename.endswith(".png"):
                    file_path = os.path.join(MEDIA_DIR, filename)
                    zipf.write(file_path, arcname=filename)
                    
                    # Add a metadata text file for each plot
                    sample_id = filename.replace("shap_sample_", "").replace(".png", "")
                    if sample_id in shap_data_store:
                        sample_data = shap_data_store[sample_id]
                        meta_content = f"Sample ID: {sample_id}\n"
                        meta_content += f"Cancer Type: {sample_data.get('cancer_type', 'Unknown')}\n"
                        meta_content += f"Subtype: {sample_data.get('subtype', 'Unknown')}\n"
                        
                        meta_filename = f"{os.path.splitext(filename)[0]}_metadata.txt"
                        meta_path = os.path.join(MEDIA_DIR, meta_filename)
                        
                        with open(meta_path, 'w') as meta_file:
                            meta_file.write(meta_content)
                        
                        zipf.write(meta_path, arcname=meta_filename)
                        
                        # Clean up temporary metadata file
                        os.remove(meta_path)

        response = FileResponse(open(zip_path, 'rb'), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
        return response

    except Exception as e:
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)

# Add a health check endpoint
@api_view(['GET'])
def health_check(request):
    """Simple health check endpoint"""
    return Response({"status": "ok"})

# Add an info endpoint to check model status
@api_view(['GET'])
def model_info(request):
    """Return information about the loaded model"""
    try:
        model_loaded = 'model' in globals() and model is not None
        scaler_loaded = 'scaler' in globals() and scaler is not None
        pca_loaded = 'pca' in globals() and pca is not None
        
        return Response({
            "model_loaded": model_loaded,
            "scaler_loaded": scaler_loaded,
            "pca_loaded": pca_loaded,
            "num_classes": len(number_to_subtype) if number_to_subtype else 0,
            "media_dir_exists": os.path.exists(MEDIA_DIR),
            "version": "1.0.0"
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# URLs should be defined in urls.py but including here for reference
urlpatterns = [
    path('api/predict_csv/', predict_csv, name='predict_csv'),
    path('api/get_shap_plot/<str:sample_id>/', get_shap_plot, name='get_shap_plot'),
    path('api/download_all_shap_plots/', download_all_shap_plots, name='download_all_shap_plots'),
    path('api/health/', health_check, name='health_check'),
    path('api/model_info/', model_info, name='model_info'),
]