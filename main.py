import network
import time
from machine import Pin
import ujson
from umqtt.simple import MQTTClient

print("Connecting to WiFi", end="")

# Esse fragmento usa MicroPython network modulo e uma WLAN classe para conectar em uma rede WiFi existente
# o wokwi usa uma simulação para se conectar ao WiFi e tem a Wokwi-GUEST SSID
# em uma placa real, precisamos colocar o SSID e a senha para nos conectar em uma rede WiFi real.

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")

# Nesse fragmento definimos os parametros que serão usados pela classe MQTTClient 
# para se conectar em um MTQQ broker server existente.
# Nesse caso, o MQTT broker é um servidor no HiveMQ Cloud.

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
client.connect() # Aqui é onde acontece a conexão MQTT 

print("Connected!")

# Definimos o IN Pin número 2 e colocamos ela em uma variavél para ler os dados do movimento
motion_pin = Pin(2, Pin.IN)

# Definimos aqui o OUT Pin número 19 e colocamos ela em uma variável para escrever os dados do movimento
led_pin = Pin(19, Pin.OUT)

while True: # esse loop infinito
    motion_pin_value = motion_pin.value() # aqui lemos a variável de movimento
    print('motion_pin_value is')
    print(motion_pin_value)


    # se o pino de movimento tem valor 1, significa que o sensor detectou movimento
    # neste caso, enviamos o valor 1 para o pino do led e o led acenderá
    # Preparamos também uma mensagem com valor 1 para o MQTT broker
    if motion_pin_value == 1:
        print('Movement detected. Turning the LED ON')
        led_pin.value(1)

        msg = {
          'movimento': 1,
          'pin': 1
        }


    # Se o pino de movimento tiver valor 0, significa que o sensor não detectou movimento
    # nesse caso, enviaremos valor 0 para o pino do led e o led apagará
    # Preparamos também uma mensagem com valor 0 para o MQTT broker
    else:
        print('Movement NOT detected. Turning the LED OFF')
        led_pin.value(0)

        msg = {
          'movimento': 0,
          'pin': 0
        }

    message = ujson.dumps(msg)

    # Enviamos aqui o código para o MQTT broker.
    MQTT_TOPIC = 'cascrisiot01/test01'
    client.publish(MQTT_TOPIC, message)

    # Aqui temos um tempo de espera no nosso loop antes de ler o pino de movimento e executar todas as ações
    time.sleep(0.5)