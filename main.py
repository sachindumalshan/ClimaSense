import machine
import network
import time
import urequests
import ujson
import dht

# WiFi credentials
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# ThingSpeak credentials
THINGSPEAK_API_KEY = "CP6FESJME94G57FQ"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Sensor Readings
dht_sensor = dht.DHT22(machine.Pin(4))
ldr_sensor = machine.ADC(1)

# Function to read analog pin
def read_ldr():
    ldr_val = ldr_sensor.read_u16()
    return ldr_val

def read_dht_sensor():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temperature, humidity

# Send data to ThingSpeak
def send_data_to_thingspeak(ldr, temperature, humidity):
  data = {
    "api_key": THINGSPEAK_API_KEY,
    "field1": ldr,
    "field2": temperature,
    "field3": humidity,
  }
  response = urequests.post(THINGSPEAK_URL, data=ujson.dumps(data),headers={"Content-Type":"application/json"})
  response.close()

# Initialize tthe Wifi connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID,WIFI_PASSWORD)

# wait for the Wi-Fi connection to establish
while not wifi.isconnected():
  time.sleep(1)

print("Connected to Wi-Fi")

if __name__ == "__main__":
  try:
    while True:
      ldr = read_ldr()
      print(f"LDR Sensor: {ldr}")
      temperature, humidity = read_dht_sensor()
      print(f"Temperature: {temperature}")
      print(f"Humidity: {humidity}")
      send_data_to_thingspeak(ldr, temperature, humidity)
      print("Data sent successfully!")
      time.sleep(20)
  except KeyboardInterrupt:
    pass
