import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/auth.css";
import twitterLogo from "../assets/LOGO.JPEG";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await axios.post("http://127.0.0.1:5000/login", {
        username,
        password,
      });

      // ✅ Store user info in sessionStorage (NOT localStorage)
      sessionStorage.setItem("userId", res.data.userId);
      sessionStorage.setItem("username", username);

      navigate("/home");

    } catch (err) {
      if (err.response?.data?.msg) {
        setError(err.response.data.msg);
      } else {
        setError("Server not reachable");
      }
    }
  };

  return (
    <div className="landing">
      <div className="left-panel">
        <img src={twitterLogo} alt="Logo" className="x-logo" />
      </div>

      <div className="right-panel">
        <h1 className="title">Happening now</h1>
        <h2 className="subtitle">Log in to your account</h2>

        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && <p className="error">{error}</p>}

          <button type="submit" className="primary-btn">
            Log in
          </button>
        </form>

        <p className="switch">
          Don’t have an account?{" "}
          <span onClick={() => navigate("/signup")}>Sign up</span>
        </p>
      </div>
    </div>
  );
}