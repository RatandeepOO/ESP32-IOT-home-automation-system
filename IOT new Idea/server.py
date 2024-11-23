from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ESP32 IP address
ESP32_URL = "http://192.168.137.133"  # Replace with your ESP32 IP address

# Weather API endpoint and key
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
WEATHER_API_KEY = "fc56de0eca164462a0a52250242111"

@app.route('/control-light', methods=['POST'])
def control_light():
    data = request.json
    command = data.get("command")
    
    if command not in ["TURN_ON", "TURN_OFF"]:
        return jsonify({"status": "error", "message": "Invalid command"})

    try:
        # Send command to ESP32
        esp_response = requests.post(f"{ESP32_URL}/light", json={"command": command})
        return jsonify(esp_response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get("location", "kashipur")
    try:
        # Fetch weather data
        response = requests.get(WEATHER_API_URL, params={"key": WEATHER_API_KEY, "q": location})
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
