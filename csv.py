import csv_config as CONFIG


def append(line):
    with open(CONFIG.CSV_PATH, "a") as logfile:
        logfile.write(line)
