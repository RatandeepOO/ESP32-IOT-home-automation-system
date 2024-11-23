const sendCommand = async (command) => {
    try {
        const response = await fetch("http://127.0.0.1:5000/control-light", {
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

const sendapiCommand = async (command) => {
    try {
        const response = await fetch("http://127.0.0.1:5000/api-control", {
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

document.getElementById("turnOn").addEventListener("click", () => sendCommand("TURN_ON"));
document.getElementById("turnOff").addEventListener("click", () => sendCommand("TURN_OFF"));
document.getElementById("Weather").addEventListener("click", () => sendapiCommand("Weather"));
