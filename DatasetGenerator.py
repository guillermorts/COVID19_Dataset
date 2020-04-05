import os
import csv
from apscheduler.schedulers.blocking import BlockingScheduler

from lib.Argentina import Argentina
from lib.China import China
from lib.England import England
from lib.France import France
from lib.Germany import Germany
from lib.Italy import Italy
from lib.Spain import Spain
from lib.USA import USA



ATTRIB_LIST = ("Date",
               "Time",
               "Country",
               "Country ISO",
               "Capital",
               "Capital ISO",
               "Cases",
               "Deaths",
               "Recovered",
               "Average Temperature",
               "O3",
               "NOx",
               "NO2",
               "NO",
               "CO2",
               "SO2")

CSV_LIST = ("Output")


class DatasetGenerator:

    def __init__(self):
        self.update_dict = {}

        # Initialize all the classe
        self.ESP = Spain.Spain()

    def update_attributes(self):
        self.ESP.update_source()
        self.ESP.update_dataset()


def check_csv_exist():
    # Create an empty file with header
    for file in CSV_LIST:
        if not os.path.exists("CSV/{}.csv".format(file)):
            with open("CSV/{}.CSV".format(file), 'w') as f:
                writer = csv.writer(f)
                writer.writerow(ATTRIB_LIST)
    if not os.path.exists("CSV/Output.csv".format(file)):
        with open("CSV/Output.csv".format(file), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(ATTRIB_LIST)


def main():
    print("Running main function")
    ds = DatasetGenerator()
    ds.update_attributes()


if __name__ == "__main__":
    print("Running...")
    check_csv_exist()
    # Update the files each hour
    # scheduler = BlockingScheduler()
    # scheduler.add_job(main, 'interval', hours=1)
    # scheduler.start()
    main()
