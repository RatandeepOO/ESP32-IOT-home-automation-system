def webpage(ssid, password):
    import network
    import socket
    import urequests
    import time
    from machine import Pin

    # Initialize relays for lights and fan
    relays = {
        "light1": Pin(16, Pin.OUT),
        "light2": Pin(5, Pin.OUT),
        "light3": Pin(19, Pin.OUT),
        "fan": Pin(23, Pin.OUT),
    }

    # Webpage generator with dynamic content
    def web_page(content=""):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ESP32 Personal Assistant</title>
            <style>
                body {{ font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #000; color: #fff; }}
                h1 {{ text-align: center; color: #61dafb; }}
                .container {{ text-align: center; padding: 20px; border-radius: 8px; background-color: #333; box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5); }}
                button {{ margin: 10px; padding: 15px 25px; font-size: 16px; color: #fff; background-color: #61dafb; border: none; border-radius: 5px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>ESP32 Personal Assistant</h1>
                {content}
                <button onclick="location.href='/light1/on'">Turn On Light 1</button>
                <button onclick="location.href='/light1/off'">Turn Off Light 1</button>
                <button onclick="location.href='/light2/on'">Turn On Light 2</button>
                <button onclick="location.href='/light2/off'">Turn Off Light 2</button>
                <button onclick="location.href='/light3/on'">Turn On Light 3</button>
                <button onclick="location.href='/light3/off'">Turn Off Light 3</button>
                <button onclick="location.href='/fan/on'">Turn On Fan</button>
                <button onclick="location.href='/fan/off'">Turn Off Fan</button>
                <button onclick="location.href='/weather'">Get Weather</button>
                <button onclick="location.href='/news'">Get News</button>
            </div>
        </body>
        </html>
        """
        return html  # Indent this correctly!


    # Fetch weather data
    def fetch_weather():
        try:
            url = "https://wttr.in/kashipur?format=%C+%t+%w"
            response = urequests.get(url)
            weather = response.text
            response.close()
            return f"<p>Weather: {weather}</p>"
        except Exception as e:
            print(f"Weather fetch error: {e}")
            return "<p>Cannot fetch weather data.</p>"

    # Fetch news headlines
    def fetch_news():
        try:
            url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=028c9fc91fd04dd99d86ba3db42db83d"
            response = urequests.get(url)
            data = response.json()
            response.close()
            headlines = [article["title"] for article in data["articles"][:5]]
            return "".join([f"<p>{headline}</p>" for headline in headlines])
        except Exception as e:
            print(f"News fetch error: {e}")
            return "<p>Cannot fetch news data.</p>"

    # Handle STT request
    def handle_stt():
        try:
            # Simulate fetching STT from a speech API (e.g., Google's STT API)
            text = "Simulated STT response: Turn on Light 1"
            print(f"STT Response: {text}")
            return f"<p>Speech Recognized: {text}</p>"
        except Exception as e:
            print(f"STT error: {e}")
            return "<p>Cannot process speech.</p>"

    # Handle TTS request
    def handle_tts():
        try:
            # Simulate TTS via an API and generate an audio file
            print("Simulating TTS audio generation.")
            return "<p>Speaking: 'Hello, I am your ESP32 assistant.'</p>"
        except Exception as e:
            print(f"TTS error: {e}")
            return "<p>Cannot process text-to-speech.</p>"

    # Handle incoming requests
    def handle_request(request):
        content = ""
        relay_states = {k: "ON" if relay.value() else "OFF" for k, relay in relays.items()}

        if "/light1/on" in request:
            relays["light1"].value(1)
        elif "/light1/off" in request:
            relays["light1"].value(0)
        elif "/light2/on" in request:
            relays["light2"].value(1)
        elif "/light2/off" in request:
            relays["light2"].value(0)
        elif "/light3/on" in request:
            relays["light3"].value(1)
        elif "/light3/off" in request:
            relays["light3"].value(0)
        elif "/fan/on" in request:
            relays["fan"].value(1)
        elif "/fan/off" in request:
            relays["fan"].value(0)
        elif "/weather" in request:
            content = fetch_weather()
        elif "/news" in request:
            content = fetch_news()
        elif "/stt" in request:
            content = handle_stt()
        elif "/tts" in request:
            content = handle_tts()

        return web_page(content, relay_states)

    # Connect to WiFi
    def connect_to_wifi(ssid, password):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, password)
        print("Connecting to WiFi...")
        while not station.isconnected():
            time.sleep(1)
        print("Connected to WiFi! IP Address:", station.ifconfig()[0])

    # Start web server
    connect_to_wifi(ssid, password)
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print("Web server started at 0.0.0.0:80")

    try:
        while True:
            cl, addr = s.accept()
            request = cl.recv(1024).decode("utf-8")
            response = handle_request(request)
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            cl.send(response)
            cl.close()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        s.close()


ssid = input("SSID :")
password = input("Password :")
webpage(ssid , password)