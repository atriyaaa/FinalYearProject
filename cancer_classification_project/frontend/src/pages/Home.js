import React from "react";
import { Link } from "react-router-dom";
import "../styles/Home.css"; // ✅ Make sure this file exists

const Home = () => {
  return (
    <div className="home-container">
      <header className="hero">
        <h1>AI-Powered Multi-Cancer Classification</h1>
        <p>Upload gene expression data to classify cancer subtypes.</p>
        <Link to="/upload" className="btn-primary">Get Started</Link>
      </header>
    </div>
  );
};

export default Home; // ✅ Ensure this is a default export
