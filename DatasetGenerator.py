from lib.Barcelona import Barcelona
from lib.Berlin import Berlin
from lib.BuenosAires import BuenosAires
from lib.London import London
from lib.Madrid import Madrid
from lib.NewYork import NewYork
from lib.Paris import Paris
from lib.SanFrancisco import SanFrancisco
from lib.Shangai import Shangai

ATTRIB_LIST = ("Date",
               "Time",
               "Country",
               "Country ISO",
               "City",
               "City ISO",
               "Cases Detected",
               "Cases",
               "Deaths",
               "Recovered",
               "Average Temperature",
               "O3",
               "NOx",
               "NO2",
               "NO",
               "CO2",
               "SO2")

def init():
    # Initialize all the classe
    BCN = Barcelona.Barcelona()
    BE = Berlin.Berlin()
    BS = BuenosAires.BuenosAires()
    LDN = London.London()
    MD = Madrid.Madrid()
    NY = NewYork.NewYork()
    PRS = Paris.Paris()
    SF = SanFrancisco.SanFrancisco()
    SGI = Shangai.Shangai()


if __name__ == '__main__':
    init()