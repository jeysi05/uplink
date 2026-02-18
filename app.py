from flask import Flask, render_template, jsonify
import random
import datetime

app = Flask(__name__)

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


# ─────────────────────────────────────────────
# API: Live Telemetry
# ─────────────────────────────────────────────

@app.route('/api/telemetry')
def telemetry():
    data = {
        "turbidity":     round(random.uniform(110, 150), 1),
        "conductivity":  round(random.uniform(650, 720), 1),
        "temperature":   round(random.uniform(27.5, 29.5), 1),
        "battery":       random.randint(95, 100),
        "gps_accuracy":  round(random.uniform(1.0, 1.5), 1),
        "satellites":    random.randint(14, 16),
        "lora_rssi":     random.randint(-95, -80),
        "timestamp":     datetime.datetime.now().strftime("%H:%M:%S")
    }
    return jsonify(data)


# ─────────────────────────────────────────────
# API: Telemetry History (for chart)
# ─────────────────────────────────────────────

@app.route('/api/telemetry/history')
def telemetry_history():
    now = datetime.datetime.now()
    labels = []
    turbidity_data = []
    conductivity_data = []

    base_turbidity    = 40
    base_conductivity = 250

    for i in range(7):
        t = now - datetime.timedelta(hours=(6 - i))
        labels.append(t.strftime("%H:%M"))
        base_turbidity    += random.uniform(5, 30)
        base_conductivity += random.uniform(20, 70)
        turbidity_data.append(round(base_turbidity, 1))
        conductivity_data.append(round(base_conductivity, 1))

    return jsonify({
        "labels":       labels,
        "turbidity":    turbidity_data,
        "conductivity": conductivity_data
    })


# ─────────────────────────────────────────────
# API: Risk Zones
# ─────────────────────────────────────────────

@app.route('/api/risk-zones')
def risk_zones():
    zones = [
        {
            "id":       "Z01",
            "level":    "high",
            "disease":  "Leptospirosis",
            "tds":      685,
            "triggers": [
                "TDS >680 μS/cm (Threshold: 500)",
                "Flood exposure >72 hours",
                "Temperature optimal for bacterial growth"
            ],
            "reference": "WHO Guidelines for Drinking Water Quality, 4th Edition (2022)"
        },
        {
            "id":       "Z02",
            "level":    "medium",
            "disease":  "Cholera",
            "tds":      420,
            "triggers": [
                "Moderate turbidity levels",
                "Recent precipitation events",
                "Population density: Medium"
            ],
            "reference": "CDC Cholera Surveillance Guidelines (2023)"
        },
        {
            "id":       "Z03",
            "level":    "low",
            "disease":  "None",
            "tds":      210,
            "triggers": [
                "Water quality within WHO standards",
                "No flood conditions",
                "Population health indicators stable"
            ],
            "reference": "Routine monitoring — no intervention required"
        }
    ]
    return jsonify(zones)


# ─────────────────────────────────────────────
# API: Network Status
# ─────────────────────────────────────────────

@app.route('/api/network-status')
def network_status():
    networks = [
        {
            "name":    "Primary Dashboard (Wi-Fi)",
            "detail":  "Real-time decision support interface • IP: 192.168.1.100",
            "status":  "CONNECTED",
            "level":   "online"
        },
        {
            "name":    "GSM SMS Gateway (SIM800L)",
            "detail":  "Targeted emergency alerts • Network: Globe Telecom",
            "status":  "OPERATIONAL",
            "level":   "online"
        },
        {
            "name":    "LoRa Mesh Network",
            "detail":  "Field sensor communication • 868MHz • 12 active nodes",
            "status":  "SYNCHRONIZED",
            "level":   "online"
        },
        {
            "name":    "Radio Broadcast (AM 702 kHz)",
            "detail":  "Mass communication channel • Coverage: 50km radius",
            "status":  "STANDBY",
            "level":   "warning"
        }
    ]
    return jsonify(networks)


# ─────────────────────────────────────────────
# API: Analytics
# ─────────────────────────────────────────────

@app.route('/api/analytics')
def analytics():
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return jsonify({
        "risk_trend": {
            "labels": days,
            "high":   [2, 4, 1, 3, 7, 5, 2],
            "medium": [5, 6, 8, 7, 9, 8, 6]
        },
        "alert_distribution": {
            "labels": ['Critical', 'High', 'Medium', 'Low'],
            "data":   [3, 12, 25, 60]
        }
    })


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────

import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)