
from . import Assistant
import pandas as pd

class Argentina:
    
    def __init__(self):
        self.casosActivos = None
        
        
    def get_all_data(self):    
        self.casosActivos = Assistant.getActiveCases('Argentina')
        
        