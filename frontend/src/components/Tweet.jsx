import { useState } from "react";

export default function Tweet() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const submitTweet = async () => {
    const token = localStorage.getItem("token");

    const res = await fetch("http://127.0.0.1:5000/tweet", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ text }),
    });

    const data = await res.json();
    setResult(data);
    setText(""); // ✅ clears old tweet
  };

  return (
    <div className="tweet-box">
      <textarea
        placeholder="What’s happening?"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={submitTweet}>Tweet</button>

      {result && (
        <div className="result">
          <p><b>Sexual:</b> {result.sexual_pred}</p>
          <p><b>Threat:</b> {result.threat_pred}</p>
          <p><b>Score:</b> {result.threat_score}</p>
        </div>
      )}
    </div>
  );
}