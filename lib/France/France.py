import sys
import Assistant

if '..\\..' not in sys.path:
    sys.path.append("..\\..")
if 'Assistant' not in sys.modules:
    import Assistant
    
import pandas as pd

class France:
    
    def __init__(self):
        self.casosActivos = None
        self.casosDiarios = None
        self.DecesosDiarios = None
        self.RecuperacionesDiarias = None
        self.all_data = None
        self.pollution = Assistant.Pollution("paris")
        
    def get_all_data(self):    
        import Assistant
        self.casosActivos = Assistant.getCases('France','Active Cases')
        self.casosDiarios = Assistant.getCases('France','Daily New Cases')
        self.DecesosDiarios = Assistant.getCases('France','Daily New Deaths')
        self.RecuperacionesDiarias = Assistant.getCases('France','Newly Recovered')
        self.dates = self.casosActivos['Date']
        self.all_data = self.casosActivos
        self.all_data['Daily New Cases'] = self.casosDiarios['Daily New Cases']
        self.all_data['Daily New Deaths'] = self.DecesosDiarios['Daily New Deaths']
        self.all_data['Newly Recovered'] = self.RecuperacionesDiarias['Newly Recovered']
        self.all_data['PM2.5'] = self.pollution.extract_data('PM2.5', self.dates)
        self.all_data['PM10'] = self.pollution.extract_data('PM10', self.dates)
        self.all_data['O3'] = self.pollution.extract_data('O3', self.dates)
        self.all_data['NO2'] = self.pollution.extract_data('NO2', self.dates)
        self.all_data['SO2'] = self.pollution.extract_data('SO2', self.dates)
        self.all_data['CO'] = self.pollution.extract_data('CO', self.dates)