# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 23:06:28 2020

@author: nbafu
"""

import pandas as pd
import re
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# Creador de asistente para llamar funciones repetitivas desde la clase Pais

# Pre: country es el nombre del pais en ingles del que se quiere extraer el
# historico de datos por día
# Post: Devuelve un pandas dataframe con los casos activos

MONT_DICT_1 = {"Jan": "01",
               "Feb": "02",
               "Mar": "03",
               "Apr": "04",
               "May": "05",
               "Jun": "06",
               "Jul": "07",
               "Aug": "08",
               "Sep": "09",
               "Oct": "10",
               "Nov": "11",
               "Dec": "12"
               }

MONT_DICT_2 = {"01": "Jan",
               "02": "Feb",
               "03": "Mar",
               "04": "Apr",
               "05": "May",
               "06": "Jun",
               "07": "Jul",
               "08": "Aug",
               "09": "Sep",
               "10": "Oct",
               "11": "Nov",
               "12": "Dec"
               }


def TranslateToGraph(tipo):
    diccionario = {'Active Cases': 'graph-active-cases-total',
                   'Daily New Cases': 'graph-cases-daily',
                   'Daily New Deaths': 'graph-deaths-daily',
                   'Newly Recovered': 'cases-cured-daily'}
    try:
        return diccionario[tipo]
    except:
        return ''
    
def GetCity(country):
    diccionario = {'Argentina': 'Buenos Aires',
                   'Spain': 'Madrid',
                   'US': 'New York',
                   'China': 'Beijing',
                   'Germany': 'Berlin',
                   'Italy': 'Rome',
                   'UK': 'London',
                   'France': 'Paris'}
    try:
        return diccionario[country]
    except:
        return ''


def getCases(country, tipo):
    TipoGrafo = TranslateToGraph(tipo)
    # Comprobamos que el tipo de búsqueda es correcto
    if (TipoGrafo == ''):
        print("Error en tipo")
        return None

    page = requests.get("https://www.worldometers.info/coronavirus/country/" + country + "/")

    # Comprobamos que la página web es correcta
    if (page.status_code != 200):
        print ("URL no encontrada")
        return None
    # Generamos el beautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # Buscamos aquellas etiquetas que tengan como atributo los indicados
    scripts = soup.find_all(attrs={'type': 'text/javascript', 'class': '', 'src': ''})

    # Buscamos entre los textos encontrados el que contenga los casos activos:
    for i in scripts:
        if (i.contents[0].find(TipoGrafo) != -1):
            chart = str(i.contents[0])
            break

    # Buscamos el patrón "data: \[.*?\]" que contiene los datos numéricos
    verifyData = re.compile(r"data: \[.*?\]", re.M)
    m = verifyData.search(chart)

    # Obtenemos los datos y los transformamos en list
    predata1 = m.group()
    predata2 = predata1[(int(predata1.find('[')) + 1):(int(predata1.find(']')))]
    data = predata2.split(",")

    # realizamos el mismo proceso para los días registrados:
    verifyCateg = re.compile(r"categories: \[.*?\]", re.M)

    m = verifyCateg.search(chart)
    predays1 = m.group()
    predays2 = predays1[(int(predays1.find('[')) + 1):(int(predays1.find(']')))]
    # Fix in the date to standaraize it
    days = []
    for day in predays2.split(","):
        day = day.replace('"', '')
        date_fix = str(day.split(" ")[1]) + "-" + str(MONT_DICT_1[day.split(" ")[0]]) + "-2020"
        days.append(date_fix)

    # Creamos la variable con las columna del país
    city = GetCity(country)

    d = {'Country': country, 'City': city, 'Date': days, tipo: data}

    df = pd.DataFrame(data=d)

    return df


class Pollution:

    def __init__(self, city="madrid"):
        self.magnitude_list = ["PM2.5",
                               "PM10",
                               "O3",
                               "NO2",
                               "SO2",
                               "CO"
                               ]
        self.url = 'https://aqicn.org/city/'
        self.driver = webdriver.Chrome()
        self.actions = ActionChains(self.driver)
        self.driver.get(self.url + city + '/')
        time.sleep(3)
        historic_data = self.driver.find_element_by_id("historic-aqidata-block")
        self.actions.move_to_element(historic_data).perform()
        time.sleep(6)
        magnitude_buttons = historic_data.find_elements_by_tag_name("li")
        self.data_dict = {}
        for buttons in magnitude_buttons:
            buttons.click()
            time.sleep(.5)
            table = historic_data.find_element_by_tag_name("table")
            table_code = table.get_attribute('innerHTML')
            data = self.process_table(table_code)
            self.data_dict.update({buttons.text: data})
        self.driver.close()
        for magnitude in self.magnitude_list:
            if not magnitude in self.data_dict.keys():
                self.data_dict.update({magnitude: None})

    def process_table(self, table_code):
        soup = BeautifulSoup(table_code, "html.parser")
        rows = soup.findAll("tr")
        data_dict = {}
        for row in rows:
            year = row['key'][:4]
            month = row['key'][4:]
            if month == "12":
                data_dict.update({year: {}})
            else:
                display = row['style'].replace("display: ", "").replace(";", "")
                cols = row.findAll("td")
                month_name = cols[0].text
                if display == "none":
                    data_dict[year].update({month_name: {}})
                    for n_day in range(1, 32):
                        data_dict[year][month_name].update({str(n_day): None})
                else:
                    data_dict[year].update({month_name: {}})
                    days_frame = cols[3].find("svg")
                    days = days_frame.findAll("text")
                    for n, day in enumerate(days):
                        if day.text == "-":
                            data_dict[year][month_name].update({str(n + 1): None})
                        else:
                            data_dict[year][month_name].update({str(n + 1): day.text})
        return data_dict

    def extract_data(self, magnitude, dates):
        try:
            assert magnitude in self.magnitude_list
        except AssertionError:
            AssertionError(
                f"The magnitude {magnitude} is not valid"
            )
        magnitude_res = []
        for date in dates:
            if not self.data_dict[magnitude]:
                magnitude_res.append("null")
            else:
                date_split = date.split("-")
                day = date_split[0].lstrip("0")
                month = date_split[1]
                year = date_split[2]
                if not self.data_dict[magnitude][year][MONT_DICT_2[month]][day]:
                    magnitude_res.append("null")
                else:
                    magnitude_res.append(self.data_dict[magnitude][year][MONT_DICT_2[month]][day])
        return magnitude_res
