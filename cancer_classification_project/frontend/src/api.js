import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api"; // ✅ Django Backend URL

export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await axios.post(`${API_BASE_URL}/predict/`, formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        return response.data; // ✅ This will return the prediction results
    } catch (error) {
        console.error("Error uploading file:", error);
        throw error;
    }
};

export const explainPrediction = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await axios.post(`${API_BASE_URL}/explain/`, formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        return response.data; // ✅ This will return SHAP values
    } catch (error) {
        console.error("Error fetching explanation:", error);
        throw error;
    }
};
