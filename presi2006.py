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

ano = 2006
ambito = "PERU"

driver = webdriver.Chrome()
driver.get('https://www.web.onpe.gob.pe/modElecciones/elecciones/resultados2006/1ravuelta/index.onpe')

data=[]
writer = codecs.open('elecciones_generales_2006.csv', 'w', "utf-8-sig")

driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="frmset"]/frame[1]'))

resultados = driver.find_element_by_xpath('//*[@class="menulink" and @href="onpe/presidente/rep_resultados_pre.onpe"]')
driver.execute_script("arguments[0].click();", resultados)
time.sleep(1)

## AMBITO: PERU #############################################################################################

driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="frmset"]/frame[2]'))
driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmubigeo"]'))

combobox1 = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[1]/select')

select = Select(combobox1)
select.select_by_value('P')

## DEPARTAMENTO #######################################

combobox2 = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/select')
select = Select(combobox2)
num_dptos = len(select.options)

for d in range(1,num_dptos):

    combobox2 = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/select')
    select = Select(combobox2)

    d1 = d + 1
    departamento = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/select/option[{0}]'.format(d1)).text
    select.select_by_index(d)

    ## PROVINCIA ########################################

    combobox3 = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[3]/select')
    select = Select(combobox3)
    num_provs = len(select.options)

    for p in range(1,num_provs):

        combobox3 = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[3]/select')
        select = Select(combobox3)

        p1 = p + 1
        provincia = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[3]/select/option[{0}]'.format(p1)).text
        select.select_by_index(p)

        ##  DISTRITO #######################################

        combobox4 = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[4]/select')
        select = Select(combobox4)
        num_dists = len(select.options)

        for di in range(1,num_dists):

            combobox4 = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[4]/select')
            select = Select(combobox4)

            di1 = di + 1
            distrito = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[4]/select/option[{0}]'.format(di1)).text
            select.select_by_index(di)

            ## RECOGER INFORMACION ###################################################################################

            consultar = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[5]/input')
            driver.execute_script("arguments[0].click();", consultar)

            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="frmset"]/frame[2]'))

            for o in range(2,26):

                if o == 22:
                    continue

                organizacion = driver.find_element_by_xpath('/html/body/form[1]/table[1]/tbody/tr[{0}]/td[1]/span'.format(o)).text
                if o==23 or o==24 or o==25:
                    votos = driver.find_element_by_xpath('/html/body/form[1]/table[1]/tbody/tr[{0}]/td[2]/div/span'.format(o)).text
                    validos = ''
                    emitidos = driver.find_element_by_xpath('/html/body/form[1]/table[1]/tbody/tr[{0}]/td[4]/div/span'.format(o)).text
                else:
                    votos = driver.find_element_by_xpath('/html/body/form[1]/table[1]/tbody/tr[{0}]/td[4]/div/span'.format(o)).text
                    validos = driver.find_element_by_xpath('/html/body/form[1]/table[1]/tbody/tr[{0}]/td[5]/div/span'.format(o)).text
                    emitidos = driver.find_element_by_xpath('/html/body/form[1]/table[1]/tbody/tr[{0}]/td[6]/div/span'.format(o)).text

                data.append((ano, ambito, departamento, provincia, distrito, organizacion, votos, validos, emitidos))

                df = pd.DataFrame(data, columns=["Ano", "Ambito", "Departamento", "Provincia", "Distrito", "Organizacion", "Votos", "Validos", "Emitidos"])
                df.to_csv('elecciones_generales_2006.csv', index=False, encoding='utf-8-sig')

            driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmubigeo"]'))
