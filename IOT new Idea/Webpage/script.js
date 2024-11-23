const SERVER_URL = "http://127.0.0.1:5000";

// Control ESP32 light
const sendCommand = async (command) => {
    try {
        const response = await fetch(`${SERVER_URL}/control-light`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ command }),
        });
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        alert("Error communicating with the server.");
        console.error(error);
    }
};

// Fetch weather
const getWeather = async () => {
    try {
        const response = await fetch(`${SERVER_URL}/weather?location=kashipur`);
        const result = await response.json();
        document.getElementById("weatherResult").innerText = `Temperature: ${result.current.temp_c}°C, Condition: ${result.current.condition.text}`;
    } catch (error) {
        alert("Error fetching weather data.");
        console.error(error);
    }
};

document.getElementById("turnOn").addEventListener("click", () => sendCommand("TURN_ON"));
document.getElementById("turnOff").addEventListener("click", () => sendCommand("TURN_OFF"));
document.getElementById("getWeather").addEventListener("click", getWeather);