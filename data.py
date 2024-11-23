from microdot import Microdot
import ujson
import network
from utime import sleep_ms, ticks_ms
from machine import Pin

# Wi-Fi credentials
ssid = "GalaxyA03s"
password = "33333333"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

print("Connecting to WiFi...")
while not wifi.isconnected():
    pass  # Wait until connected

print("Connected to WiFi:", wifi.ifconfig())

# Initialize the server and LED pin
app = Microdot()
led = Pin(2, Pin.OUT)

# Handle CORS preflight (OPTIONS request)
@app.route('/blink', methods=['OPTIONS'])
def options_handler(request):
    return '', 204, {  # 204 = No Content
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

# Handle POST requests to blink the LED
@app.route('/blink', methods=['POST'])
def blink_handler(request):
    start = ticks_ms()  # Start timer for performance logging
    try:
        # Parse JSON data from the request
        data = ujson.loads(request.body)
        blinks = int(data.get('blinks', 0))  # Get 'blinks' value, default is 0

        # Cap the number of blinks to prevent overloading
        blinks = min(blinks, 10)  # Maximum 10 blinks allowed

        # Blink the LED the specified number of times
        for _ in range(blinks):
            led.on()
            sleep_ms(200)  # LED ON for 200ms
            led.off()
            sleep_ms(200)  # LED OFF for 200ms

        # Return success response with CORS headers
        elapsed = ticks_ms() - start  # Calculate elapsed time
        print(f"Request handled in {elapsed} ms")
        return f"Successfully blinked {blinks} times!", 200, {
            'Access-Control-Allow-Origin': '*',
        }

    except Exception as e:
        # Handle errors and return response with CORS headers
        print("Error:", str(e))
        return f"Error: {str(e)}", 500, {
            'Access-Control-Allow-Origin': '*',
        }

# Basic route for testing
@app.route('/')
def hello(request):
    return "Hello, Microdot is running!", 200

# Start the server
app.run(debug=True)  # Removed 'threaded' argument
