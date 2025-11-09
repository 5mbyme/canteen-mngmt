import React from "react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="py-3 m-3 mt-5">
      <div className="container text-center">
        <p className="mb-0" style={{ fontSize: "14px", letterSpacing: "1px" }}>
          © {currentYear} Canteen Management System. All rights reserved.
        </p>
        <p 
          className="mb-0" 
          style={{ 
            fontSize: "12px", 
            marginTop: "8px",
            fontFamily: "'Press Start 2P', cursive",
            color: "#00ffff"
          }}
        >
          Developed with <i className="fas fa-heart text-danger"></i> by{" "}
          <span style={{ color: "#ffff00" }}>
            Aswin Radhakrishnan & Vedant Mishra
          </span>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
