from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("postgresql://birthdaygift_db_user:H00jHnBe7sfWYdGeqXPmyb4YxK7elzMD@dpg-d8cpc8e8bjmc73ca69hg-a.oregon-postgres.render.com/birthdaygift_db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Rezension(db.Model):                                      #einfach klasse für rezensionen
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

@app.route("/api/rezensionen", methods=["GET"])                 
def get_rezensionen():
    rezensionen = Rezension.query.order_by(Rezension.created_at.desc()).all() #Rezensionen aus datenbank abrufen 

    return jsonify([                                                        #json für frontend bauen und senden (enthält alle reznsionen)
        {
            "id": r.id,
            "user": r.user,
            "content": r.content,
            "created_at": r.created_at.isoformat()
        }
        for r in rezensionen
    ])

@app.route("/api/rezensionen", methods=["POST"])            #bekommen daten und speichern was wir brauchen in der datenbank bevor wir ok an frontend zurückschicken
def add_rezension():
    data = request.get_json()

    content = data.get("content", "").strip()
    user = data.get("user", "").strip()

    # Validierung
    if not content:
        return jsonify({"error": "Leerer Inhalt"}), 400

    if len(content) > 500:
        return jsonify({"error": "Text zu lang"}), 400

    if len(user) > 50:
        return jsonify({"error": "Username zu lang"}), 400

    new_message = Rezension(
        content=content,
        user=user
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)