import { useState, useEffect } from "react";
import axios from "axios";
import "../styles/home.css";
import homeIcon from "../assets/home.jpeg";
import exploreIcon from "../assets/explore.jpeg";
import { Link } from "react-router-dom";
import messagesIcon from "../assets/messages.jpeg";
import profileIcon from "../assets/profile.jpeg";
import twitterIcon from "../assets/twitter.jpeg";
export default function Home() {
  const [tweet, setTweet] = useState("");
  const [tag, setTag] = useState("");
  const [tweets, setTweets] = useState([]);
  const [userId, setUserId] = useState(null);
  const [username, setUsername] = useState("");

  const BASE_URL = "http://127.0.0.1:5000";

  // ===============================
  // DUMMY INTERNATIONAL NEWS
  // ===============================
  const news = [
    {
      id: 1,
      title: "Global Markets Rally After Economic Boost",
      source: "Reuters",
      time: "2h ago",
    },
    {
      id: 2,
      title: "UN Climate Summit Calls for Immediate Action",
      source: "BBC World",
      time: "5h ago",
    },
    {
      id: 3,
      title: "Tech Giants Announce AI Collaboration",
      source: "CNN International",
      time: "8h ago",
    },
    {
      id: 4,
      title: "SpaceX Launches New Satellite Mission",
      source: "Al Jazeera",
      time: "10h ago",
    },
  ];

  // ===============================
  // LOAD USER FROM sessionStorage
  // ===============================
  useEffect(() => {
    const storedId = sessionStorage.getItem("userId");
    const storedName = sessionStorage.getItem("username");
    const firstletter=storedName?storedName.charAt(0):"U";
    if (!storedId) {
      alert("User not logged in");
      return;
    }

    setUserId(parseInt(storedId));
    setUsername(storedName);
  }, []);

  // ===============================
  // FETCH TWEETS (ONLY THIS USER)
  // ===============================
  const fetchTweets = async (uid) => {
    try {
      const res = await axios.get(`${BASE_URL}/tweets/${uid}`);
      setTweets(res.data);
    } catch (err) {
      console.log("Error fetching tweets:", err);
    }
  };

  // ===============================
  // LOAD DATA WHEN userId READY
  // ===============================
  useEffect(() => {
    if (userId) {
      fetchTweets(userId);
    }
  }, [userId]);

  // ===============================
  // SUBMIT TWEET
  // ===============================
  const submitTweet = async () => {
    if (!userId) {
      alert("User not logged in");
      return;
    }

    if (!tweet.trim()) {
      alert("Tweet cannot be empty");
      return;
    }

    try {
      const taggedUsers = tag
        .split(",")
        .map((u) => u.trim())
        .filter((u) => u);

      const res = await axios.post(`${BASE_URL}/tweet`, {
        userId: userId,
        content: tweet,
        taggedUsernames: taggedUsers,
      });

      alert(res.data.msg);

      setTweet("");
      setTag("");

      fetchTweets(userId);

    } catch (err) {
      console.log("Error posting tweet:", err);
      alert(err.response?.data?.msg || "Failed to post tweet");
    }
  };
// ===============================
// FORMAT TIME LIKE TWITTER
// ===============================

  return (
    <div className="layout">
      {/* LEFT SIDEBAR */}
      <div className="sidebar">
      <img src={twitterIcon} alt="Twitter" />

  <ul className="menu">
    <li className="menu_home">
  <Link to="/feed">
    <img src={homeIcon} alt="Home" className="home-icon" />
  </Link>
</li>

    <li className="menu-item">
      <img src={exploreIcon} alt="Explore" />
    </li>

    <li className="menu-item">
  <Link to="/messages">
    <img src={messagesIcon} alt="Messages" />
  </Link>
</li>


    <li className="menu-item">
      <img src={profileIcon} alt="Profile" />
      
    </li>
  </ul>

  <button className="post-btn">Post</button>
</div>

      {/* CENTER FEED */}
      <div className="feed">
        <div className="feed-header">
          <h2>Welcome {username}!!!</h2>
        </div>

        {/* Tweet Box */}
        <div className="feed">
  

  {/* NEW WRAPPER */}
  <div className="content-row">

    {/* Tweet Box */}
    <div className="tweet-box">
      <textarea
        placeholder="What's happening?"
        value={tweet}
        onChange={(e) => setTweet(e.target.value)}
      />

      <input
        placeholder="@tag users (comma-separated)"
        value={tag}
        onChange={(e) => setTag(e.target.value)}
      />

      <div className="tweet-action">
        <button onClick={submitTweet}>Post</button>
      </div>
    </div>

    {/* Safety Box */}
    <div className="safety-box">
      <h3>🔐 Use Social Media Safely</h3>
      <ul>
        <li>Think before you post.</li>
        <li>Avoid sharing personal information.</li>
        <li>Report abusive or harmful content.</li>
        <li>Respect others online.</li>
        <li>Stay positive and responsible.</li>
      </ul>
    </div>

  </div>
</div>

       <div className="trending-section">
  <h3>🔥 Trending Hashtags</h3>

  <div className="hashtag-item">#Jananayagan</div>
  <div className="hashtag-item">#IndiaElections</div>
  <div className="hashtag-item">#TechNews</div>
  <div className="hashtag-item">#WorldCup</div>
  <div className="hashtag-item">#AIRevolution</div>
</div>
      </div>

      {/* RIGHT PANEL - NEWS */}
      <div className="right-panel">
        <div className="premium-box">
          <h3>Subscribe to Premium</h3>
          <p>Get rid of ads, boost replies and unlock features.</p>
          <button>Subscribe</button>
        </div>

        <div className="notifications">
          <h3>🌍 International News</h3>

          {news.map((item) => (
            <div key={item.id} className="notification">
              <strong>{item.title}</strong>
              <div style={{ fontSize: "12px", color: "#536471", marginTop: "4px" }}>
                {item.source} • {item.time}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}