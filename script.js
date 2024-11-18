fetch('http://192.168.181.234/blink', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ blinks: parseInt(document.getElementById('blinkInput').value, 10) }),
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.text();
})
.then(data => {
    document.getElementById('response').textContent = `ESP32 Response: ${data}`;
})
.catch(error => {
    document.getElementById('response').textContent = `Error: ${error.message}`;
});
