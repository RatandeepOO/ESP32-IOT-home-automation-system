const sendRequest = async (endpoint) => {
    try {
        const response = await fetch(`http://192.168.137.133:80${endpoint}`);
        const data = await response.json();
        if (data.weather) {
            alert(`Weather: ${data.weather}`);
        } else if (data.news) {
            alert(`News Headlines:\n${data.news.join("\n")}`);
        } else if (data.message) {
            alert(data.message);
        } else {
            alert("Unknown response from ESP32");
        }
    } catch (error) {
        alert("Error communicating with ESP32");
        console.error(error);
    }
};

const sendapiCommand = async (command) => {
        try {
            const response = await fetch("http://127.0.0.1:5000/weather", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ command }),
            });
            const result = await response.json();
            alert(result.message);
        } catch (error) {
            alert("Error communicating with server.");
            console.error(error);
        }
};

document.getElementById("turnOn1").addEventListener("click", () => sendRequest("/light1/on"));
document.getElementById("turnOff1").addEventListener("click", () => sendRequest("/light1/off"));
document.getElementById("turnOn2").addEventListener("click", () => sendRequest("/light2/on"));
document.getElementById("turnOff2").addEventListener("click", () => sendRequest("/light2/off"));
document.getElementById("turnOn3").addEventListener("click", () => sendRequest("/light3/on"));
document.getElementById("turnOff3").addEventListener("click", () => sendRequest("/light3/off"));
document.getElementById("fanOn").addEventListener("click", () => sendRequest("/fan/on"));
document.getElementById("fanOff").addEventListener("click", () => sendRequest("/fan/off"));
document.getElementById("getWeather").addEventListener("click", () => sendapiCommand("/weather"));
document.getElementById("getNews").addEventListener("click", () => sendRequest("/news"));
