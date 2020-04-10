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

import pandas as pd

import Assistant

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
               "PM2.5",
               "PM10",
               "O3",
               "NO2",
               "SO2",
               "CO")

COUNTRY_DICT = {"Argentina": "Buenos Aires",
                "China": "Beijing",
                "England": "London",
                "France": "Paris",
                "Germany": "Berlin",
                "Italy": "Rome",
                "Spain": "Madrid",
                "United States of America": "NewYork"
                }

CSV_LIST = ("Output")


class DatasetGenerator:

    def __init__(self):
        self.update_dict = {}

        # Initialize all the classe
        self.ESP = Spain.Spain()
        self.ARG = Argentina.Argentina()
        self.CHI = China.China()
        self.ENG = England.England()
        self.FRA = France.France()
        self.GER = Germany.Germany()
        self.ITA = Italy.Italy()
        self.USA = USA.USA()
        self.ALL = None
    
    def get_data(self):
        print("Getting ESP Data...")
        self.ESP.get_all_data()
        print("Getting ARG Data...")
        self.ARG.get_all_data()
        print("Getting CHI Data...")
        self.CHI.get_all_data()
        print("Getting ENG Data...")
        self.ENG.get_all_data()
        print("Getting FRA Data...")
        self.FRA.get_all_data()
        print("Getting GER Data...")
        self.GER.get_all_data()
        print("Getting ITA Data...")
        self.ITA.get_all_data()
        print("Getting USA Data...")
        self.USA.get_all_data()
        print("Concatenating Data...")
        self.ALL = pd.concat([self.ESP.all_data,self.ARG.all_data,
                              self.CHI.all_data,self.ENG.all_data,
                              self.FRA.all_data,self.GER.all_data,
                              self.ITA.all_data,self.USA.all_data], ignore_index = True)
        
    def print_to_csv(self):
        if (self.ALL is not None):
            self.ALL.to_csv("output.csv")
            print("CSV Exported")
        else:
            print("Datos no cargados")
        return 0


def check_csv_exist():
    # Create an empty file with header
    for file in CSV_LIST:
        if not os.path.exists("CSV/{}.csv".format(file)):
            with open("CSV/{}.csv".format(file), 'w') as f:
                writer = csv.writer(f)
                writer.writerow(ATTRIB_LIST)
    if not os.path.exists("CSV/Output.csv".format(file)):
        with open("CSV/Output.csv".format(file), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(ATTRIB_LIST)


def main():
    print("Running main function")
    ds = DatasetGenerator()
    ds.get_data()
    ds.print_to_csv()


if __name__ == "__main__":
    print("Running...")
    check_csv_exist()
    main()
