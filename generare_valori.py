import random
import time
import json
import paho.mqtt.client as mqtt  # Corectarea importului
import signal
import sys


# Function to simulate temperature readings
def simulate_temperature():
    return round(random.uniform(20.0, 25.0), 2)

# Function to simulate air quality readings
def simulate_air_quality():
    return round(random.uniform(0.0, 100.0), 2)

# MQTT Configuration
mqtt_broker = "mqtt.beia-telemetrie.ro"
mqtt_port = 1883
mqtt_topic = "/training/device/mironcosmin/"

client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)

def signal_handler(sig, frame):
    print('Disconnecting from MQTT broker...')
    client.disconnect()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    while True:
        temperature = simulate_temperature()
        air_quality = simulate_air_quality()

        sensor_data = json.dumps({
            "temperature": temperature,
            "air_quality": air_quality
        })

        client.publish(mqtt_topic, sensor_data)
        print(f"Published: {sensor_data}")

        time.sleep(20)

except KeyboardInterrupt:
    signal_handler(None, None)

print("Simulation stopped")
