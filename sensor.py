import re


def path():
    lib_path = "/sys/bus/w1/devices/"
    sensor_names_file = open("/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves", "r")
    sensor = sensor_names_file.readline()
    if sensor:
        sensor_names_file.close()

    return lib_path + sensor.strip() + '/w1_slave'


SENSOR_PATH = path()


# Temperatur ermitteln und Wert value zurckgeben
def read():
    a = open(SENSOR_PATH, 'r')  # Ermittelten Sensor lesen
    value_raw = a.readline()

    if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", value_raw):  # Erste Zeile auf "YES" am Ende uberprufen
        value_raw = a.readline()
        m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", value_raw)  # Wert aus zweiter Zeile prufen
    if m:
        value = float(m.group(2)) / 1000.0
    a.close()
    return value  # Ruckgabewert "value" definieren
