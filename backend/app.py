from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from final_prediction import final_predict
import os
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "Backend_Server", "database.db")


# ===============================
# DATABASE CONNECTION
# ===============================
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ===============================
# LOGIN ROUTE (IMPORTANT)
# ===============================
@app.route("/")
def home():
    return "Twitter Harassment Backend Running"
    
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({
                "msg": "Login successful",
                "userId": user["id"]
            })
        else:
            return jsonify({"msg": "Invalid credentials"}), 401

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"msg": "Server error"}), 500


# ===============================
# POST TWEET (WITH ML MODERATION)
# ===============================
@app.route("/tweet", methods=["POST"])
def post_tweet():
    try:
        data = request.json
        user_id = data.get("userId")
        content = data.get("content")
        tagged_usernames = data.get("taggedUsernames", [])

        if not user_id or not content:
            return jsonify({"msg": "Missing data"}), 400

        # 🔥 RUN ML MODEL
        result = final_predict(content)
        final_label = result["final_label"]
        print("ML RESULT:", final_label)
        # 🚫 BLOCK severe case
        if final_label == "sexual_threat":
            return jsonify({"msg": "Tweet blocked due to severe violation"}), 403

        conn = get_db()
        cursor = conn.cursor()

        # ===============================
        # SAVE TWEET
        # ===============================
        cursor.execute("""
    INSERT INTO tweets (user_id, content, final_label)
    VALUES (?, ?, ?)
""", (user_id, content, final_label))

        conn.commit()
        tweet_id = cursor.lastrowid

        flagged = final_label != "non_sexual_non_threat"

        # ===============================
        # SAVE TAGS
        # ===============================
        tagged_ids = []

        for username in tagged_usernames:
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                tagged_id = user["id"]
                tagged_ids.append(tagged_id)

                cursor.execute("""
                    INSERT INTO tags (tweet_id, tagged_id)
                    VALUES (?, ?)
                """, (tweet_id, tagged_id))

        # ===============================
        # AUTHOR WARNING (if flagged)
        # ===============================
        if flagged:
            cursor.execute("""
                INSERT INTO notifications (user_id, tweet_id, type)
                VALUES (?, ?, ?)
            """, (user_id, tweet_id, "warning"))

        # ===============================
        # ALERT TAGGED USERS (if flagged)
        # ===============================
        if flagged:
            for tagged_id in tagged_ids:
                cursor.execute("""
                    INSERT INTO notifications (user_id, tweet_id, type)
                    VALUES (?, ?, ?)
                """, (tagged_id, tweet_id, "alert"))

        conn.commit()
        conn.close()

        return jsonify({
            "msg": "Tweet processed successfully",
            "category": final_label
        })

    except Exception as e:
        print("POST TWEET ERROR:", e)
        return jsonify({"msg": "Server error"}), 500


# ===============================
# GET USER TWEETS
# ===============================
@app.route("/tweets/<int:user_id>", methods=["GET"])
def get_tweets(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, content, created_at
            FROM tweets
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))

        tweets = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify(tweets)

    except Exception as e:
        print("GET TWEETS ERROR:", e)
        return jsonify([])
# ===============================
# SIGNUP ROUTE
# ===============================
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400

        conn = get_db()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return jsonify({"msg": "Username already exists"}), 400

        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return jsonify({"msg": "Signup successful"}), 201

    except Exception as e:
        print("SIGNUP ERROR:", e)
        return jsonify({"msg": "Server error"}), 500

# ===============================
# GET NOTIFICATIONS
# ===============================
@app.route("/notifications/<int:user_id>", methods=["GET"])
def get_notifications(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
    SELECT notifications.id,
           notifications.type,
           tweets.content,
           tweets.created_at,
           tweets.id as tweet_id,
           tweets.final_label,
           users.username AS attacker_username
    FROM notifications
    JOIN tweets ON notifications.tweet_id = tweets.id
    JOIN users ON tweets.user_id = users.id
    WHERE notifications.user_id = ?
    ORDER BY notifications.id DESC
""", (user_id,))

        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append({
                "id": row["id"],
                "type": row["type"],
                "message": row["content"],
                "created_at": row["created_at"],
                "final_label": row["final_label"],
                "attacker_username": row["attacker_username"]
            })

        return jsonify(result)

    except Exception as e:
        print("GET NOTIFICATIONS ERROR:", e)
        return jsonify([])
# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)