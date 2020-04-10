import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import Assistant


import sys
if '..\\..' not in sys.path:
    sys.path.append("..\\..")

if 'Assistant' not in sys.modules:
    import Assistant


class Spain:
    
    
    def __init__(self):
        self.download_path = str(os.path.join(Path.home(), "Downloads"))
        self.current_path = os.path.abspath("temp")
        self.casosActivos = None
        self.casosDiarios = None
        self.DecesosDiarios = None
        self.RecuperacionesDiarias = None
        self.all_data = None
        self.pollution = Assistant.Pollution("madrid")

    def get_all_data(self):
        import Assistant
        self.casosActivos = Assistant.getCases('Spain','Casos Activos')
        self.casosDiarios = Assistant.getCases('Spain','Nuevos Casos Diarios')
        self.DecesosDiarios = Assistant.getCases('Spain','Decesos Diarios')
        self.RecuperacionesDiarias = Assistant.getCases('Spain','Recuperaciones Diarias')
        self.dates = self.casosActivos['Date']
        self.all_data = self.casosActivos
        self.all_data['Nuevos Casos Diarios'] = self.casosDiarios['Nuevos Casos Diarios']
        self.all_data['Decesos Diarios'] = self.DecesosDiarios['Decesos Diarios']
        self.all_data['Recuperaciones Diarias'] = self.RecuperacionesDiarias['Recuperaciones Diarias']
        self.all_data['PM2.5'] = self.pollution.extract_data('PM2.5', self.dates)
        self.all_data['PM10'] = self.pollution.extract_data('PM10', self.dates)
        self.all_data['O3'] = self.pollution.extract_data('O3', self.dates)
        self.all_data['NO2'] = self.pollution.extract_data('NO2', self.dates)
        self.all_data['SO2'] = self.pollution.extract_data('SO2', self.dates)
        self.all_data['CO'] = self.pollution.extract_data('CO', self.dates)
        print(self.all_data)


