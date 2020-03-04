import ntptime
import network
import utime

from sht20 import SHT20
from wdt_simple import WDT
from machine import ADC, Pin

from config import CONFIG
from influxdb import update_influxdb

LED_OFF = 1
LED_ON = 0


class EnvMonitor:
    def __init__(self):
        self.wdt_cnt = 0

        self.sht = SHT20(scl_pin=5, sda_pin=4)
        self.adc = ADC(0)
        self.val = self.adc.read() * 3.3 / 1024.0
        self.dev_id = int(self.val / 0.5)               # set Nodemcu id
        self.led = Pin(2, Pin.OUT)

        # Set to station mode for connecting to network
        self.sta_if = network.WLAN(network.STA_IF)

        if CONFIG['WIFI']['AP']:
            ap_if = network.WLAN(network.AP_IF)
            ap_if.config(essid=CONFIG['WIFI']['AP_SSID'] + str(self.dev_id),
                         authmode=network.AUTH_WPA_WPA2_PSK,
                         password=CONFIG['WIFI']['AP_PASSWORD'])

            ap_if.active(True)

    def connect(self):
        if not self.sta_if.isconnected():
            print('Connecting to network...')
            self.sta_if.active(True)
            self.sta_if.connect(CONFIG['WIFI']['STA_SSID'], CONFIG['WIFI']['STA_PASSWORD'])

            # Wait until connected
            while not self.sta_if.isconnected():
                pass
            print('Network connected!')

            # Synchronise the system time using NTP
            ntptime.settime()

    def blink(self):
        for sw in [LED_ON, LED_OFF]:
            self.led.value(sw)
            if CONFIG['BRIGHTNESS'] == 'HIGH':
                utime.sleep_ms(10)
            else:
                utime.sleep_us(10)

    def measure(self):
        if self.wdt_cnt >= 65535:
            self.wdt_cnt = 0
        else:
            self.wdt_cnt += 1

        # # get time
        # utc8 = utime.time() + 28800  # UTC + 8
        # s = utime.localtime(utc8)
        # t = '{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(s[0], s[1], s[2], s[3], s[4], s[5])

        # get SHT20 data
        temperature = self.sht.get_temperature()
        humidity = self.sht.get_relative_humidity()
        # print('{}, temp: {}, humi: {}'.format(wdt_cnt, temperature, humidity))

        return {'wdt': self.wdt_cnt,
                'id': self.dev_id,
                'temperature': temperature,
                'humidity': humidity
                }

    def send(self, datas):
        print('Sending data...')
        dev_str = 'Dev_' + str(self.dev_id)
        tables = ['Temperature', 'Humidity', 'Watchdog']
        devs = [dev_str, dev_str, dev_str]
        datas = [datas['temperature'], datas['humidity'], datas['wdt']]
        resp = update_influxdb(tables, devs, datas)

        print('Response: {}'.format(resp.status_code))
        print('')
        self.blink()


def main():
    env = EnvMonitor()
    print('Nodemcu {} Start'.format(env.dev_id))

    for _ in range(10):
        env.blink()
        utime.sleep_ms(50)

    wdt = WDT(10000)
    while True:
        env.connect()
        wdt.feed()
        datas = env.measure()
        env.send(datas)
        utime.sleep(1)


if __name__ == '__main__':
    main()
