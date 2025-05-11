from flask import Flask, request, jsonify

app = Flask(__name__)
events = []

@app.route('/event', methods=['POST'])
def receive_event():
    data = request.get_json()
    print("Eveniment primit:", data)
    events.append(data)
    return jsonify({"status": "ok"}), 200

@app.route('/json')
def status_json():
    if events:
        return jsonify(events[-1])
    else:
        return jsonify({"type": "N/A", "time": "--:--:--"})
    
@app.route('/')
def status():
    return """
    <html>
    <head>
        <title>Status PIR</title>
        <script>
        function updateStatus() {
            fetch('/json')
                .then(res => res.json())
                .then(data => {
                    document.getElementById("type").textContent = data.type;
                    document.getElementById("time").textContent = data.time;
                });
        }

        setInterval(updateStatus, 500);  // actualizare la 0.5 secunde
        </script>
    </head>
    <body>
        <h1>Status Sistem PIR</h1>
        <h1><b>Ultimul eveniment:</b> <span id="type">...</span></h1>
        <h1><b>Ora:</b> <span id="time">--:--:--</span></h1>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("Pornește serverul Flask...")
    app.run(host='0.0.0.0', port=5000, threaded=True)

