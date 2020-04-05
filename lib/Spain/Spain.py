import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path


class Spain:

    def __init__(self):
        self.download_path = str(os.path.join(Path.home(), "Downloads"))
        self.current_path = os.path.abspath("temp")

    def update_source(self):
        with webdriver.Chrome() as driver:
            driver.get("https://covid19.isciii.es/")
            column = driver.find_element_by_class_name("column")
            link = column.find_element_by_tag_name("a")
            link.click()
            time.sleep(4)
            os.replace(self.download_path + "/serie_historica_acumulados.csv",
                       self.current_path + "/serie_historica_acumulados.csv")
            # Clean last lines of the file
            with open("temp/serie_historica_acumulados.csv", "r") as f:
                lines = f.readlines()
            with open("temp/serie_historica_acumulados.csv", "w") as f:
                for line in lines[:-2]:
                    f.write(line)

    def update_dataset(self, path=""):
        source_file = open('temp/serie_historica_acumulados.csv')
        end_file = open('CSV/Output.csv')
        csv_source = csv.reader(source_file, delimiter=',')
        csv_end = csv.reader(end_file, delimiter=',')
        if True:
            # In case the output file doesn't contain previous information fulfill the lines
            print("He entrado")
            for row in csv_source:
                print(row)
                if row[0] in ("MD", "CT"):
                    if row["CCAA Codigo ISO"] == "MD":
                        city = "Madrid"
                    elif row["CCAA Codigo ISO"] == "CT":
                        city = "BARCELONA"
                    else:
                        city = "N/A"
                    csv_end.append({"Date": row["Fecha"],
                                    "Country": "Spain",
                                    "Country ISO": "ESP",
                                    "City": city,
                                    "City ISO": row["CCAA Codigo ISO"],
                                    "Cases": row["Casos"],
                                    "Deaths": row["Fallecidos"],
                                    })
        else:  #
            # The file already contains information, so we update the information and add new files
            pass


if __name__ == "__main__":
    ESP = Spain()
    ESP.update_source()
    ESP.update_dataset("temp/serie_historica_acumulados.csv")