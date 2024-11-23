def webpage(ssid, password): 
    import network
    import socket
    import urequests
    import time
    from machine import Pin

    # Initialize relays for lights and fan
    light_relay1 = Pin(16, Pin.OUT)
    light_relay2 = Pin(5, Pin.OUT)
    light_relay3 = Pin(19, Pin.OUT)
    fan_relay = Pin(23, Pin.OUT)

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
                <button onclick="location.href='/fan/on'">Turn On Light 4</button>
                <button onclick="location.href='/fan/off'">Turn Off Light 4</button>
                <button onclick="location.href='/weather'">Get Weather</button>
                <button onclick="location.href='/news'">Get News</button>
            </div>
        </body>
        </html>
        """
        return html

    def fetch_weather():
        try:
            # Request weather data from wttr.in for Kashipur
            url = "https://wttr.in/kashipur?format=%C+%t+%w"  # Format as: condition, temperature, wind
            response = urequests.get(url)
            weather = response.text
            response.close()
            return f"<p>Weather: {weather}</p>"
        except Exception as e:
            print(e)
            return "<p>Sorry, cannot fetch the weather.</p>"

    def fetch_news():
        try:
            response = urequests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=028c9fc91fd04dd99d86ba3db42db83d")
            data = response.json()
            response.close()
            headlines = [article['title'] for article in data['articles'][:5]]
            news_content = "<br>".join(f"<p>{headline}</p>" for headline in headlines)
            return news_content
        except Exception as e:
            print(e)
            return "<p>News data unavailable</p>"

    def handle_request(request):
        content = ""
        if '/light1/on' in request:
            light_relay1.value(1)
        elif '/light1/off' in request:
            light_relay1.value(0)
        elif '/light2/on' in request:
            light_relay2.value(1)
        elif '/light2/off' in request:
            light_relay2.value(0)
        elif '/light3/on' in request:
            light_relay3.value(1)
        elif '/light3/off' in request:
            light_relay3.value(0)
        elif '/fan/on' in request:
            fan_relay.value(1)
        elif '/fan/off' in request:
            fan_relay.value(0)
        elif '/weather' in request:
            content = fetch_weather()
        elif '/news' in request:
            content = fetch_news()
        return content

    def connect_to_wifi(ssid, password):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, password)

        while not station.isconnected():
            print("Connecting to WiFi...")
            time.sleep(1)
        print("Connected to WiFi!")
        print("IP Address:", station.ifconfig()[0])

    # Connect to WiFi
    connect_to_wifi(ssid, password)

    # Set up the web server
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print("Web server started...")

    try:
        while True:
            try:
                cl, addr = s.accept()
                request = cl.recv(1024)
                request = str(request)
                content = handle_request(request)
                response = web_page(content)
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
                cl.close()
            except Exception as e:
                print(e)
                continue
    finally:
        s.close()  # Ensure the socket is closed on program exit

ssid = input("SSID :")
password = input("Password :")
webpage(ssid , password)