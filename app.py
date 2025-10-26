from flask import Flask,request, jsonify,render_template
from flask_cors import CORS
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Simulating device statuses for demonstration purposes
devices = {
    "bedroom": {"light": False, "fan": False, "heater": False},
    "kitchen": {"light": False, "fan": False, "heater": False},
    "hall": {"light": False, "fan": False},
    "store_room": {"light": False},
    "bathroom": {"light": False, "fan": False},
    "washarea": {"light": False}
}

def simulate_device_change():
    # This function randomly changes device status to simulate real-time changes
    for room in devices:
        for device in devices[room]:
            devices[room][device] = random.choice([False, False])
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api/status', methods=['GET'])
def get_status():
    # simulate_device_change()  # Simulate changes for demonstration
    return jsonify(devices)


@app.route('/api/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    intent_name = data['queryResult']['intent']['displayName']
    
    # Handle intents
    if intent_name == 'TurnOnAppliance':
        room = data['queryResult']['parameters']['Room']
        appliance = data['queryResult']['parameters']['Appliance']
        
        # Check if room and appliance exist
        if room not in devices or appliance not in devices[room]:
            response_text = f"The {appliance} in the {room} does not exist."
            print(response_text)
            return jsonify(fulfillmentMessages=[{"text": {"text": [response_text]}}])

        # Check if appliance is already on
        if devices[room][appliance]:
            response_text = f"The {appliance} in the {room} is already on."
            print(response_text)
            return jsonify(fulfillmentMessages=[{"text": {"text": [response_text]}}])

        devices[room][appliance] = True
        response_text = f"Turning on the {appliance} in the {room}."
        print(response_text)
        return jsonify(fulfillmentMessages=[{"text": {"text": [response_text]}}])

    elif intent_name == 'TurnOffAppliance':
        room = data['queryResult']['parameters']['Room']
        appliance = data['queryResult']['parameters']['Appliance']
        
        # Check if room and appliance exist
        if room not in devices or appliance not in devices[room]:
            response_text = f"The {appliance} in the {room} does not exist."
            print(response_text)
            return jsonify(fulfillmentMessages=[{"text": {"text": [response_text]}}])

        # Check if appliance is already off
        if not devices[room][appliance]:
            response_text = f"The {appliance} in the {room} is already off."
            print(response_text)
            return jsonify(fulfillmentMessages=[{"text": {"text": [response_text]}}])

        devices[room][appliance] = False
        response_text = f"Turning off the {appliance} in the {room}."
        print(response_text)
        return jsonify(fulfillmentMessages=[{"text": {"text": [response_text]}}])

    return jsonify({})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
