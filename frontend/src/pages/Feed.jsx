import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/home.css";

export default function Feed() {
  const [tweets, setTweets] = useState([]);
  const [username, setUsername] = useState("");
  const [userId, setUserId] = useState(null);

  const BASE_URL = "http://127.0.0.1:5000";

  useEffect(() => {
    const storedId = sessionStorage.getItem("userId");
    const storedName = sessionStorage.getItem("username");

    if (!storedId) {
      alert("User not logged in");
      return;
    }

    setUserId(parseInt(storedId));
    setUsername(storedName);
  }, []);

  useEffect(() => {
    if (userId) {
      fetchTweets(userId);
    }
  }, [userId]);

  const fetchTweets = async (uid) => {
    try {
      const res = await axios.get(`${BASE_URL}/tweets/${uid}`);
      setTweets(res.data);
    } catch (err) {
      console.log("Error fetching tweets:", err);
    }
  };

  return (
    <div className="layout">
      <div className="feed">
        <div className="feed-header">
          <h2>{username}'s Tweets</h2>
        </div>

        {tweets.map((t) => (
          <div key={t.id} className="tweet-card">
            <div className="avatar">
              {username ? username.charAt(0).toUpperCase() : "U"}
            </div>

            <div className="tweet-body">
              <div className="tweet-header">
                <span className="tweet-name">{username}</span>
                <span className="tweet-username">@{username}</span>
                <span className="tweet-time"> · {t.created_at}</span>
              </div>

              <div className="tweet-text">
                {t.content}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}