import RPi.GPIO as GPIO
from time import sleep
import datetime
from firebase import firebase
from hx711 import HX711
import Adafruit_ADS1x15
import math
import wiringpi
import Adafruit_ADS1x15

GPIO.setmode(GPIO.BCM)
hx = HX711(dout_pin=5, pd_sck_pin=6)
hx.set_scale_ratio(10)  # Ganti scale_ratio dengan nilai kalibrasi Anda
hx.reset()
pin = 4
GPIO.setup(pin, GPIO.IN)  # Setup pin GPIO sebagai input
GPIO.setwarnings(False)

adc = Adafruit_ADS1x15.ADS1115()
GAIN1 = 1
GAIN2 = 2
values = [0]*100

from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

firebase = firebase.FirebaseApplication('https://database-srgt-default-rtdb.firebaseio.com/', None)

def update_firebase():
    temperature = sensor.get_temperature()
    if temperature is not None:
        str_temp = ' {:.2f} °C '.format(temperature)
        str_brt = ' {:.2f} *gr '.format(berat)
        str_vlt = ' {:.2f} *a  '.format(ampere)
        str_amp = ' {:.2f} *v  '.format(volt)
        print('Temp={:.2f} °C'.format(temperature))
        print('brt={:.2f}*'.format(berat))
        print('amp={:.2f}*'.format(ampere))
        print('vlt={:.2f}*'.format(volt))
    else:
        print('Failed to get reading. Try again!')
        sleep(5)

    data = {"suhu": str_temp, "berat": str_brt, "voltage": str_vlt, "ampere": str_amp}
    response = firebase.patch('srgt', data)
    #response = firebase.post("suhu": temperature, "berat": berat)
    print("Firebase response:", response)

try:
    while True:
        berat = hx.get_raw_data_mean()
        print(berat)
        for i in range(100):
        values[i] = adc.read_adc(0, gain=GAIN2)
        #print(math.ceil(4.2))
        print("OFF")
        #print(math.ceil(sum(values) / len(values)))
        print(max(values))
        update_firebase()
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()  # Membersihkan pin GPIO saat program dihentikan
    print("Program terminated.")

