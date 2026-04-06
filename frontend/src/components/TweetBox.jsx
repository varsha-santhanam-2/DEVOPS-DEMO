import { useState } from "react";
import api from "../api/api";

export default function TweetBox({ onTweet }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleTweet = async () => {
    if (!text.trim()) return;

    setLoading(true);
    await api.post("/tweets", { text });
    setText("");
    setLoading(false);
    onTweet(); // reload tweets
  };

  return (
    <div className="tweet-box">
      <textarea
        placeholder="What is happening?!"
        value={text}
        onChange={(e) => setText(e.target.value)}
        maxLength={280}
      />
      <button onClick={handleTweet} disabled={loading}>
        {loading ? "Posting..." : "Tweet"}
      </button>
    </div>
  );
}