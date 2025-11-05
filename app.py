from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY


# Supabase configuration
SUPABASE_URL = "https://noezhsobhxdjwidejrwl.supabase.co/rest/v1/accidents"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5vZXpoc29iaHhkandpZGVqcndsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyODIwMzgsImV4cCI6MjA3Nzg1ODAzOH0.NFXMwopwR1IpAVGdvxVs0__Hn4k_zW6MWe448t8s9tg"

app = Flask(__name__)

# Function to calculate severity
def check_severity(sensor_data):
    accel = sensor_data['accelerometer']
    magnitude = sum([x**2 for x in accel])**0.5
    return "Severe" if magnitude > 15 else "Not Severe"

# API endpoint
@app.route("/accident-data", methods=["POST"])
def accident_data():
    data = request.json

    severity = check_severity(data['sensors'])

    # Prepare data for Supabase
    headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
    }


    payload = {
        "car_number": data['car_number'],
        "time": data.get('time', datetime.utcnow().isoformat()),
        "lat": data['location']['lat'],
        "long": data['location']['long'],
        "sensors": json.dumps(data['sensors']),
        "severity": severity
    }

    # Store data in Supabase
    response = requests.post(SUPABASE_URL, headers=headers, json=payload)
    print("Supabase status:", response.status_code)
    print("Supabase reply:", response.text)
    print("Supabase Response:", response.status_code, response.text)

    # Just print instead of SMS
    if severity == "Severe":
        print(f"⚠️ Accident Detected! Car {data['car_number']} at {data['location']['lat']}, {data['location']['long']}")
    else:
        print("✅ Not severe accident.")

    return jsonify({"status": "success", "severity": severity})

if __name__ == "__main__":
    app.run(debug=True)
