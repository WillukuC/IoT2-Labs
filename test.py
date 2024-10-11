#!/usr/bin/env python
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config
import json
import ADC0832
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D26)

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, GPIO.LOW)

def customCallback(client, userdata, message):
	print("Received a new message: ")

	decoded_msg = message.payload.decode("utf-8")
	msg = json.loads(decoded_msg)

	print(msg)
	print("from topic: ")
	print(message.topic)

	if msg["temperature"] > 26.0:
		GPIO.output(19, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(19, GPIO.LOW)

	print("----------------\n\n")
def init():
	ADC0832.setup()
	# Set time
	date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
	print(f"Timestamp:{date}")

myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
if myMQTTClient.connect():
	print('AWS connection succeeded')

myMQTTClient.subscribe('champlain/republish', 1, customCallback)
time.sleep(5)


def loop():
	while True:
		try:
			# Get moisture from the soil moisture sensor
			res = ADC0832.getADC(0)
			moisture = 255 - res

			# Get temperature from the DHT-11 sensor
			temperature_c = float(dhtDevice.temperature)


			payload=json.dumps({"temperature": temperature_c, "moisture": moisture})
			myMQTTClient.publish('champlain/sensor/102/data', payload, 1)

			message = myMQTTClient.subscribe('champlain/republish', 1, customCallback)
		except RuntimeError as error:
			# Errors happen fairly often, DHT's are hard to read, just keep going
			print(error.args[0])
			time.sleep(2.0)
			continue
		except Exception as error:
			dhtDevice.exit()
			raise error
		time.sleep(2.0)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt:
		ADC0832.destroy()
		print('Ending process')
