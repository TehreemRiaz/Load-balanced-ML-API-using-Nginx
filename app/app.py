from flask import Flask, request, jsonify, send_from_directory
import joblib
import os
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('iris_model.pkl')
print("Model loaded successfully!")

def get_container_id():
    with open("/proc/self/cgroup") as f:
        for line in f:
            if 'docker' in line:
                container_id = line.strip().split("/")[-1]
                return container_id
    return "Unknown"

@app.route("/")
def serve_interface():
    return send_from_directory(os.getcwd(), 'templates/index.html')

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    inputs = data.get("inputs")
    inputs_array = np.array(inputs)
    predictions = model.predict(inputs_array).tolist()
    container_id = get_container_id()
    
    response = {
        "predictions": predictions,
        "container_id": container_id  # Return the container ID
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
