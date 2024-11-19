from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route('/send-data', methods=['POST'])
def receive_data():
    data = request.json
    print(f"Received data: {data}")  # Print received data to console
    return jsonify({"status": "success", "message": "Data received", "received": data})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # Run server on localhost
