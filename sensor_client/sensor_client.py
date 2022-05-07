import time
import schedule
import mysql.connector
from datetime import datetime
import DHT_lib
import board
from adafruit_bme280 import basic as adafruit_bme280


def setup_db():
    with mysql.connector.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='rootpass',
                                 database='sensor') as cnx:
        cur = cnx.cursor(prepared=True)
        table_ddl = 'CREATE TABLE IF NOT EXISTS raw_data (\
time TIMESTAMP(6) NOT NULL UNIQUE,\
simple_check SMALLINT NOT NULL,\
temperature_simple FLOAT(4),\
humidity_simple FLOAT(4),\
temperature FLOAT(4),\
humidity FLOAT(4),\
pressure FLOAT(4),\
height FLOAT(4)\
);'
        cur.execute(table_ddl)
        cnx.commit()

    return


dht = DHT_lib.DHT(11)


def get_simple_measurements():
    chk = dht.read_DHT11()
    # if chk is 0:
    #     print('ok')
    # print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f " % (chk, dht.humidity, dht.temperature))

    return [chk, dht.humidity, dht.temperature]


i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1022.


def get_extended_measurements():
    return [bme280.temperature, bme280.humidity, bme280.pressure, bme280.altitude]


def get_measurements():
    simple_measurements = get_simple_measurements()
    extended_measurements = get_extended_measurements()
    return simple_measurements + extended_measurements


def insert_measures():
    print('Starting local_connect()')
    with mysql.connector.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='rootpass',
                                 database='sensor') as cnx:
        cur = cnx.cursor(prepared=True)

        insert_query = "INSERT INTO raw_data \
    (time, simple_check, temperature_simple, humidity_simple, temperature, humidity, pressure, height) \
    values(%s, %s, %s, %s, %s, %s, %s);"

        date_time = datetime.now()
        measures: list[object] = get_measurements()
        params = [date_time] + measures
        cur.execute(insert_query, params)

        # query = 'SELECT * FROM raw_data;'
        # cur.execute(query)
        # for el in cur:
        #     print(el)

        cnx.commit()

    return


if __name__ == '__main__':
    setup_db()
    schedule.every(5).seconds.do(insert_measures)
    while True:
        schedule.run_pending()
        time.sleep(.1)
