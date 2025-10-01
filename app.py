from flask import Flask, jsonify
from tasks import add_dummy_bet

app = Flask(__name__)

@app.route("/")
def home():
    # Example Celery call
    result = add_dummy_bet.delay(2, 3)
    return jsonify({"task_id": result.id, "status": "Task submitted!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
