from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder="frontend")
CORS(app)


def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    role TEXT,
                    wallet TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS gigs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    client_id INTEGER,
                    student_id INTEGER,
                    status TEXT
                )''')
    conn.commit()
    conn.close()

init_db()


@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# ---------- API ROUTES ----------
# Create a new user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name, role, wallet) VALUES (?, ?, ?)",
              (data["name"], data["role"], data["wallet"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201

# Create a gig
@app.route("/api/gigs", methods=["POST"])
def create_gig():
    data = request.json
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO gigs (title, description, client_id, student_id, status) VALUES (?, ?, ?, ?, ?)",
              (data["title"], data.get("description", ""), data.get("client_id"), data.get("student_id"), "open"))
    conn.commit()
    conn.close()
    return jsonify({"message": "Gig created successfully", "id": 1}), 201

# Get all gigs
@app.route("/api/gigs", methods=["GET"])
def get_gigs():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM gigs")
    rows = c.fetchall()
    conn.close()
    gigs = [{"id": r[0], "title": r[1], "description": r[2], "client_id": r[3],
             "student_id": r[4], "status": r[5]} for r in rows]
    return jsonify(gigs)

if __name__ == "__main__":
    app.run(debug=True)
