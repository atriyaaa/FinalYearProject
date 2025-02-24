import React, { useState } from "react";
import { uploadFile } from "../api"; // ✅ Import API function
import "../styles/Upload.css";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert("Please upload a file first.");
      return;
    }

    setLoading(true);
    try {
      const response = await uploadFile(file);
      setPrediction(response.prediction);
    } catch (error) {
      alert("Error predicting cancer type.");
    }
    setLoading(false);
  };

  return (
    <div className="upload-container">
      <h2>Upload Gene Expression Data</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv,.tsv" onChange={handleFileChange} />
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Predict Cancer Type"}
        </button>
      </form>

      {prediction && (
        <div className="result">
          <h3>Predicted Cancer Subtype:</h3>
          <p>{prediction}</p>
        </div>
      )}
    </div>
  );
};

export default Upload;
