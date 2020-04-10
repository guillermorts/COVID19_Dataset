import Assistant
import sys

if '..\\..' not in sys.path:
    sys.path.append("..\\..")
if 'Assistant' not in sys.modules:
    import Assistant
    
import pandas as pd

class England:
    
    def __init__(self):
        self.casosActivos = None
        self.casosDiarios = None
        self.DecesosDiarios = None
        self.RecuperacionesDiarias = None
        self.all_data = None
        self.pollution = Assistant.Pollution("london")
        
    def get_all_data(self): 
        import Assistant
        self.casosActivos = Assistant.getCases('UK','Casos Activos')
        self.casosDiarios = Assistant.getCases('UK','Nuevos Casos Diarios')
        self.DecesosDiarios = Assistant.getCases('UK','Decesos Diarios')
        self.dates = self.casosActivos['Date']
        self.RecuperacionesDiarias = None
        self.all_data = self.casosActivos
        self.all_data['Nuevos Casos Diarios'] = self.casosDiarios['Nuevos Casos Diarios']
        self.all_data['Decesos Diarios'] = self.DecesosDiarios['Decesos Diarios']
        self.all_data['Recuperaciones Diarias'] = None
        self.all_data['PM2.5'] = self.pollution.extract_data('PM2.5', self.dates)
        self.all_data['PM10'] = self.pollution.extract_data('PM10', self.dates)
        self.all_data['O3'] = self.pollution.extract_data('O3', self.dates)
        self.all_data['NO2'] = self.pollution.extract_data('NO2', self.dates)
        self.all_data['SO2'] = self.pollution.extract_data('SO2', self.dates)
        self.all_data['CO'] = self.pollution.extract_data('CO', self.dates)