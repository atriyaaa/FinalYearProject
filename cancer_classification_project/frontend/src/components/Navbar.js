import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css"; // ✅ Make sure this file exists

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1>CancerXAI</h1>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/upload">Upload</Link></li>
        <li><Link to="/results">Results</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar; // ✅ Ensure this is a default export
