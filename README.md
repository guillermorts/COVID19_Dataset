# Practice 1: Web scraping

## Description

This practice has been done under the context of the subject _Tipología y ciclo de vida de los datos_, that belongs to the Master degree of Data Science from _Universitat Oberta de Catalunya_. In this practice, is applied the web scraping technique using Python programming language to extract data from the webs _https://www.worldometers.info/_ y  _https://aqicn.org/_ to generate a dataset.

## Authors

This activity has been done as a team project developed by:
* **Nicola Bafundi** - [PurpleBooth](https://github.com/nico152)
* **Guillermo Orts** - [PurpleBooth](https://github.com/guillermorts)

## Source code files

* **DataSetGenerator.py**: Main script for the generation of the dataset. Initiate the scraping process and generate the .csv file.
* **Assistant.py**: contains the implementation of general methods used in other classes to extract COVID-19 and pollution data.
* **lib/Argentina.py**: contains the implementation of the class _Argentina_ witch methods generate the data from _Argentina_ and _Buenos Aires_.
* **lib/China.py**: contains the implementation of the class _China_ which methods generate the data from _China_ and _Beijing_.
* **lib/England.py**: contains the implementation of the class _England_ which methods generate the data from _England_ and _London_.
* **lib/France.py**: contains the implementation of the class _France_ which methods generate the data from _France_ and _Paris_.
* **lib/Germany.py**: contains the implementation of the class _Germany_ which methods generate the data from _Germany_ and _Berlin_.
* **lib/Italy.py**: contains the implementation of the class _Italy_ which methods generate the data from _Italy_ and _Rome_.
* **lib/Spain.py**: contains the implementation of the class _Spain_ which methods generate the data from _Spain_ and _Madrid_.
* **lib/USA.py**: contains the implementation of the class _USA_ which methods generate the data from _USA_ and _New York_.

## Pluggins

* **chromedriver.exe**: This driver is required for the execution of the Selenium functions.

## Output

* **CSV/COVID19_Pollution_Dataset.csv**: Is the output file containing the dataset generated in _.csv_ format.

## Other resources

* **Practica_1.pdf**: Document containing the response of the answer to the questions posed in the statement of practice one of the subject _Tipología y ciclo de vida de los datos_.



## Recursos

1. Lawson, R. (2015). _Web Scraping with Python_. Packt Publishing Ltd. Chapter 2. Scraping the Data.
2. Mitchel, R. (2015). _Web Scraping with Python: Collecting Data from the Modern Web_. O'Reilly Media, Inc. Chapter 1. Your First Web Scraper.