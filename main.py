import network
import time
from machine import Pin
import ujson
from umqtt.simple import MQTTClient

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")


MQTT_CLIENT_ID = b'abc'
MQTT_BROKER = b'e3c0fc8531864dbb992e918fc43b028c.s1.eu.hivemq.cloud'
MQTT_USER = b'cascrisbern@gmail.com'
MQTT_PASSWORD = b'Ojghf9@77'
MQTT_PORT = 8883

client = MQTTClient(MQTT_CLIENT_ID,
                    MQTT_BROKER,
                    user=MQTT_USER,
                    password=MQTT_PASSWORD,
                    port=MQTT_PORT,
                    ssl=True,
                    ssl_params = {'server_hostname': b'e3c0fc8531864dbb992e918fc43b028c.s1.eu.hivemq.cloud'}
                    )
client.connect()

print("Connected!")

motion_pin = Pin(2, Pin.IN)
led_pin = Pin(19, Pin.OUT)

while True:
    motion_pin_value = motion_pin.value()
    print('motion_pin_value is')
    print(motion_pin_value)

    if motion_pin_value == 1:
        print('Movement detected. Turning the LED ON')
        led_pin.value(1)

        msg = {
          'movimento': 1,
          'pin': 1
        }

    else:
        print('Movement NOT detected. Turning the LED OFF')
        led_pin.value(0)

        msg = {
          'movimento': 0,
          'pin': 0
        }

    message = ujson.dumps(msg)

    MQTT_TOPIC = 'cascrisiot01/test01'
    client.publish(MQTT_TOPIC, message)

    time.sleep(0.5)