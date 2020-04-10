# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 23:06:28 2020

@author: nbafu
"""

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
import pandas as pd

#Creador de asistente para llamar funciones repetitivas desde la clase Pais

#Pre: country es el nombre del pais en ingles del que se quiere extraer el
# historico de datos por día
#Post: Devuelve un pandas dataframe con los casos activos

def TranslateToGraph(tipo):
    diccionario = {'Casos Activos' : 'graph-active-cases-total',
                   'Nuevos Casos Diarios': 'graph-cases-daily',
                   'Decesos Diarios': 'graph-deaths-daily',
                   'Recuperaciones Diarias':'cases-cured-daily' }
    try:
        return diccionario[tipo]
    except:
        return ''
    
    


def getCases(country,tipo):
    
    TipoGrafo = TranslateToGraph(tipo)
    #Comprobamos que el tipo de búsqueda es correcto
    if (TipoGrafo == ''):
        print("Error en tipo")
        return None
    
    
    page = requests.get("https://www.worldometers.info/coronavirus/country/" + country + "/")
    
    #Comprobamos que la página web es correcta
    if (page.status_code != 200) :
        print ("URL no encontrada")
        return None
    #Generamos el beautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")
    
    #Buscamos aquellas etiquetas que tengan como atributo los indicados
    scripts = soup.find_all(attrs={'type':'text/javascript','class':'','src':''})
    
    # Buscamos entre los textos encontrados el que contenga los casos activos:
    for i in scripts:  
        if (i.contents[0].find(TipoGrafo) != -1):
            chart = str(i.contents[0])
            break
    
    #Buscamos el patrón "data: \[.*?\]" que contiene los datos numéricos
    verifyData= re.compile(r"data: \[.*?\]",re.M)
    m = verifyData.search(chart)
    
    #Obtenemos los datos y los transformamos en list
    predata1 = m.group()
    predata2 = predata1[(int(predata1.find('['))+1):(int(predata1.find(']')))]
    data = predata2.split(",")
    
    #realizamos el mismo proceso para los días registrados:
    verifyCateg= re.compile(r"categories: \[.*?\]",re.M)
    
    m = verifyCateg.search(chart)
    predays1 = m.group()
    predays2 = predays1[(int(predays1.find('['))+1):(int(predays1.find(']')))]
    days = predays2.split(",")
    
    #Creamos la variable con las columna del país
    countryCol = [country]*len(days)
    
    d = {'Country' : countryCol, 'Fecha': days, tipo:data}
    
    df = pd.DataFrame(data = d)
    
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
                    for n_day in range(1, 31):
                        data_dict[year][month_name].update({n_day: None})
                else:
                    data_dict[year].update({month_name: {}})
                    days_frame = cols[3].find("svg")
                    days = days_frame.findAll("text")
                    for n, day in enumerate(days):
                        if day.text == "-":
                            data_dict[year][month_name].update({str(n+1): None})
                        else:
                            data_dict[year][month_name].update({str(n+1): day.text})
        return data_dict







