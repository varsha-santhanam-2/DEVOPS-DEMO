// server.js
const express = require("express");
const cors = require("cors");
const sqlite3 = require("sqlite3").verbose();

const app = express();
app.use(cors());
app.use(express.json());

// Connect to SQLite database (creates database.db in same folder if not exists)
const db = new sqlite3.Database("database.db", (err) => {
  if (err) console.error("DB connection error:", err.message);
  else console.log("Connected to SQLite database");
});

// Create 'users' table and insert test user
db.serialize(() => {
  // 1️⃣ Create users table if it doesn't exist
  db.run(
    `CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      password TEXT
    )`,
    (err) => {
      if (err) console.error("Table creation error:", err.message);
      else console.log("Users table ready");
    }
  );

  // 2️⃣ Insert a test user
  db.run(
    `INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)`,
    ["testuser", "1234"],
    (err) => {
      if (err) console.error("Insert test user error:", err.message);
      else console.log("Test user ready (username: testuser, password: 1234)");
    }
  );
});

// Login endpoint
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  db.get(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    [username, password],
    (err, row) => {
      if (err) return res.status(500).json({ msg: "Database error" });
      if (!row) return res.status(401).json({ msg: "Invalid credentials" });

      // Login successful → return a dummy token
      res.json({ token: "dummy-token-123" });
    }
  );
});

// ----------------- SIGNUP -----------------
app.post("/signup", (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ msg: "Username and password required" });
  }

  db.run(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    [username, password],
    function (err) {
      if (err) {
        if (err.message.includes("UNIQUE")) {
          return res.status(409).json({ msg: "Username already exists" });
        }
        return res.status(500).json({ msg: "Database error" });
      }

      // Success → return user id
      res.json({ msg: "Signup successful", userId: this.lastID });
    }
  );
});
// Start server
app.listen(5000, () => console.log("Server running on http://127.0.0.1:5000"));
