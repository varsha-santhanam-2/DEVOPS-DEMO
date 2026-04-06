export default function TweetCard({ tweet }) {
  return (
    <div className="tweet-card">
      <strong>@{tweet.username}</strong>
      <p>{tweet.text}</p>

      <div className="labels">
        <span className={tweet.threat_pred === "THREAT" ? "threat" : "safe"}>
          {tweet.threat_pred} ({tweet.threat_score})
        </span>
        <span>{tweet.sexual_pred}</span>
      </div>
    </div>
  );
}