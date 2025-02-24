import axios from "axios";
import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Title, Tooltip } from 'chart.js';
import React, { useState } from "react";
import { Bar } from "react-chartjs-2"; // ✅ Ensure `react-chartjs-2` is installed
import "../styles/Results.css"; // ✅ Ensure this file exists

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Results = () => {
  const [shapValues, setShapValues] = useState([]);
  const [genes, setGenes] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchExplanation = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/explain/");
      setShapValues(response.data.shap_values);
      setGenes(response.data.genes);
    } catch (error) {
      console.error("Error fetching SHAP values:", error);
    }
    setLoading(false);
  };

  return (
    <div className="results-container">
      <h2>Feature Importance (SHAP Values)</h2>
      <button onClick={fetchExplanation} disabled={loading}>
        {loading ? "Loading..." : "Show Explanation"}
      </button>

      {shapValues.length > 0 && (
        <Bar
          data={{
            labels: genes,
            datasets: [
              {
                label: "SHAP Values",
                data: shapValues[0], // Taking first row as an example
                backgroundColor: "rgba(75, 192, 192, 0.6)",
              }
            ]
          }}
        />
      )}
    </div>
  );
};

export default Results; // ✅ Ensure this is a default export
