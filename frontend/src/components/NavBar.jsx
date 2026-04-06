import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/navbar.css";

export default function Navbar() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false); // for mobile hamburger

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login"); // redirect to login/home
  };

  const toggleMenu = () => setOpen(!open);

  return (
    <nav className="sidebar">
      {/* Logo and Hamburger */}
      <div className="sidebar-top">
        <button className="hamburger" onClick={toggleMenu}>
          ☰
        </button>
      </div>

      {/* Navigation buttons */}
      <div className={`nav-links ${open ? "active" : ""}`}>
        <button className="nav-btn active" onClick={() => navigate("/")}>
          Home
        </button>
        <button className="nav-btn" onClick={() => navigate("/explore")}>
          Explore
        </button>
        <button className="nav-btn" onClick={() => navigate("/profile")}>
          Profile
        </button>
      </div>

      {/* Logout at the bottom */}
      <div className="sidebar-bottom">
        <button className="logout" onClick={logout}>
          Logout
        </button>
      </div>
    </nav>
  );
}