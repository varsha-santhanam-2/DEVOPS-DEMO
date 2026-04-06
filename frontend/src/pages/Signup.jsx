import { useState } from "react";
import API from "../api/api";
import "../styles/twitter.css";
import "../styles/signup.css";

export default function Signup() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const submit = async () => {
    setError("");
    try {
      const res = await API.post("/signup", form);
      alert(res.data.msg + " Login now.");
      window.location.href = "/login";
    } catch (err) {
      if (err.response && err.response.data && err.response.data.msg) {
        setError(err.response.data.msg);
      } else {
        setError("Server not reachable");
      }
    }
  };

  return (
    <div className="auth">
      <h2>Sign up</h2>
      <input
        placeholder="Username"
        onChange={(e) => setForm({ ...form, username: e.target.value })}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={submit}>Sign up</button>
    </div>
  );
}
