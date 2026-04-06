// createDatabase.js
const sqlite3 = require("sqlite3").verbose();

// Create (or open) database
const db = new sqlite3.Database("database.db", (err) => {
  if (err) console.error("DB connection error:", err.message);
  else console.log("Connected to SQLite database");
});

// Create tables
db.serialize(() => {
  // Tweets table
  // Add final_label column to tweets (if not exists)
db.run(
  `ALTER TABLE tweets ADD COLUMN final_label TEXT`,
  (err) => {
    if (err) {
      if (err.message.includes("duplicate column name")) {
        console.log("final_label column already exists");
      } else {
        console.error("Error adding final_label column:", err.message);
      }
    } else {
      console.log("final_label column added successfully");
    }
  }
);
});

// Close database
db.close((err) => {
  if (err) console.error(err.message);
  else console.log("Database setup complete and connection closed.");
});
