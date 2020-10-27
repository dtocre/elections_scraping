# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import codecs
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

## ENTRAR A LA PAGINA WEB ###################################################################################

ano = 2016
ambito = "PERU"

driver = webdriver.Chrome()
driver.get('https://www.web.onpe.gob.pe/modElecciones/elecciones/elecciones2016/PRPCP2016/Resultados-Ubigeo-Presidencial.html#posicion')

data=[]
writer = codecs.open('elecciones_generales_2016.csv', 'w', "utf-8-sig")

## AMBITO: PERU #############################################################################################

combobox1 = driver.find_element_by_xpath('//*[@id="cdgoAmbito"]')

select = Select(combobox1)
select.select_by_value('P')

## DEPARTAMENTO #######################################

combobox2 = driver.find_element_by_xpath('//*[@id="cdgoDep"]')
select = Select(combobox2)
num_dptos = len(select.options)

for d in range(1,num_dptos):

    combobox2 = driver.find_element_by_xpath('//*[@id="cdgoDep"]')
    select = Select(combobox2)

    d1 = d + 1
    departamento = driver.find_element_by_xpath('//*[@id="cdgoDep"]/option[{0}]'.format(d1)).text
    select.select_by_index(d)

    ## PROVINCIA ########################################

    combobox3 = driver.find_element_by_xpath('//*[@id="cdgoProv"]')
    select = Select(combobox3)
    num_provs = len(select.options)

    for p in range(1,num_provs):

        combobox3 = driver.find_element_by_xpath('//*[@id="cdgoProv"]')
        select = Select(combobox3)

        p1 = p + 1
        provincia = driver.find_element_by_xpath('//*[@id="cdgoProv"]/option[{0}]'.format(p1)).text
        select.select_by_index(p)

        ##  DISTRITO #######################################

        combobox4 = driver.find_element_by_xpath('//*[@id="cdgoDist"]')
        select = Select(combobox4)
        num_dists = len(select.options)

        for di in range(1,num_dists):

            combobox4 = driver.find_element_by_xpath('//*[@id="cdgoDist"]')
            select = Select(combobox4)

            di1 = di + 1
            distrito = driver.find_element_by_xpath('//*[@id="cdgoDist"]/option[{0}]'.format(di1)).text
            select.select_by_index(di)

            ## RECOGER INFORMACION ###################################################################################

            for o in range(2,16):

                try:
                    organizacion = driver.find_element_by_xpath('//*[@id="page-wrap"]/table/tbody/tr[{0}]/td[1]'.format(o)).text
                    votos = driver.find_element_by_xpath('//*[@id="page-wrap"]/table/tbody/tr[{0}]/td[2]'.format(o)).text
                    validos = driver.find_element_by_xpath('//*[@id="page-wrap"]/table/tbody/tr[{0}]/td[3]'.format(o)).text
                    emitidos = driver.find_element_by_xpath('//*[@id="page-wrap"]/table/tbody/tr[{0}]/td[4]'.format(o)).text
                except NoSuchElementException:
                    organizacion = ''
                    votos = ''
                    validos = ''
                    emitidos = ''

                data.append((ano, ambito, departamento, provincia, distrito, organizacion, votos, validos, emitidos))

                df = pd.DataFrame(data, columns=["Ano", "Ambito", "Departamento", "Provincia", "Distrito", "Organizacion", "Votos", "Validos", "Emitidos"])
                df.to_csv('elecciones_generales_2016.csv', index=False, encoding='utf-8-sig')

            ## VOTOS EN BLANCO Y NULOS

            for o in range(2,4):

                organizacion = driver.find_element_by_xpath('//div[@class="col-xs-12 pbot30"]/div/table/tbody/tr[{0}]/td[1]'.format(o)).text
                votos = driver.find_element_by_xpath('//div[@class="col-xs-12 pbot30"]/div/table/tbody/tr[{0}]/td[2]'.format(o)).text
                validos = ''
                emitidos = driver.find_element_by_xpath('//div[@class="col-xs-12 pbot30"]/div/table/tbody/tr[{0}]/td[4]'.format(o)).text

                data.append((ano, ambito, departamento, provincia, distrito, organizacion, votos, validos, emitidos))

                df = pd.DataFrame(data, columns=["Ano", "Ambito", "Departamento", "Provincia", "Distrito", "Organizacion", "Votos", "Validos", "Emitidos"])
                df.to_csv('elecciones_generales_2016.csv', index=False, encoding='utf-8-sig')
