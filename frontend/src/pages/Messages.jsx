import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/home.css";

export default function Messages() {
  const [notifications, setNotifications] = useState([]);
  const [username, setUsername] = useState("");
  const [userId, setUserId] = useState(null);

  const BASE_URL = "http://127.0.0.1:5000";

  // Load logged in user
  useEffect(() => {
    const storedId = sessionStorage.getItem("userId");
    const storedName = sessionStorage.getItem("username");

    if (!storedId) {
      alert("User not logged in");
      window.location.href = "/login";
      return;
    }

    setUserId(parseInt(storedId));
    setUsername(storedName);
  }, []);

  // Fetch notifications
  useEffect(() => {
    if (userId) {
      fetchNotifications(userId);
    }
  }, [userId]);

  const fetchNotifications = async (uid) => {
    try {
      const res = await axios.get(`${BASE_URL}/notifications/${uid}`);
      setNotifications(res.data);
    } catch (err) {
      console.log("Error fetching notifications:", err);
    }
  };

  return (
    <div className="layout">
      <div className="feed">
        <div className="feed-header">
          <h2>{username}'s Notifications</h2>
        </div>

        <div className="tweets-list">
          {notifications.length === 0 && (
            <p className="empty">No notifications yet</p>
          )}

          {notifications.map((n) => (
            <div key={n.id} className="tweet-card">
              <div className="avatar">
                {username ? username.charAt(0).toUpperCase() : "U"}
              </div>

              <div className="tweet-content">
                <div className="tweet-header">
                  <span className="tweet-name">
                    {n.type === "warning"
                      ? "⚠️ Warning"
                      : `🚨 Alert from ${n.attacker_username}`}
                  </span>
                </div>

                <p>{n.message}</p>

                <div
                  style={{
                    marginTop: "6px",
                    fontSize: "13px",
                    color: "#536471",
                  }}
                >
                  Reason for harm: <strong>It's a {n.final_label} tweet .</strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}