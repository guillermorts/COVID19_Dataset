# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 23:06:28 2020

@author: nbafu
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

#Creador de asistente para llamar funciones repetitivas desde la clase Pais

#Pre: country es el nombre del pais en ingles del que se quiere extraer el
# historico de datos por día
#Post: Devuelve un pandas dataframe con los casos activos

def getActiveCases(country):
    
    page = requests.get("https://www.worldometers.info/coronavirus/country/" + country + "/")
    print()
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
        if (i.contents[0].find('graph-active-cases-total') != -1):
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
    
    d = {'Country' : countryCol, 'Fecha': days, 'Casos Activos':data}
    
    df = pd.DataFrame(data = d)
    
    return df
    
    
    