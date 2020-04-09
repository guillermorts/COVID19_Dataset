import sys
if '..\\..' not in sys.path:
    sys.path.append("..\\..")
if 'Assistant' not in sys.modules:
    import Assistant
import pandas as pd

class USA:
    
    def __init__(self):
        self.casosActivos = None
        self.casosDiarios = None
        self.DecesosDiarios = None
        self.RecuperacionesDiarias = None
        self.all_data = None
        
    def get_all_data(self):   
        import Assistant
        self.casosActivos = Assistant.getCases('US','Casos Activos')
        self.casosDiarios = Assistant.getCases('US','Nuevos Casos Diarios')
        self.DecesosDiarios = Assistant.getCases('US','Decesos Diarios')
        self.RecuperacionesDiarias = None
        self.all_data = self.casosActivos
        self.all_data['Nuevos Casos Diarios'] = self.casosDiarios['Nuevos Casos Diarios']
        self.all_data['Decesos Diarios'] = self.DecesosDiarios['Decesos Diarios']
        self.all_data['Recuperaciones Diarias'] = None