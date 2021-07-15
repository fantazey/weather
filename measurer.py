import os
import datetime
import sqlite3
import Adafruit_DHT

PATH = os.path.dirname(os.path.abspath(__file__))
PIN = 4
DB = os.path.join(PATH,"db.sqlite")


def setup():
    connector = sqlite3.connect(DB)
    connector.execute("CREATE TABLE IF NOT EXISTS temperature(date TEXT, temperature REAL, humidity REAL)")
    connector.commit()
    connector.close()


def insert_row(date_string, temp, humidity):
    connector = sqlite3.connect(DB)
    connector.execute("INSERT INTO temperature VALUES (\"%s\", %f, %f)" % (date_string, temp, humidity))
    connector.commit()
    connector.close()


def read_data(pin, sensor_version = 11):
    return Adafruit_DHT.read_retry(sensor_version, pin)


if __name__ == '__main__':
    setup()
    humidity, temp = read_data(PIN)
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print date, temp
    insert_row(date, temp, humidity)

