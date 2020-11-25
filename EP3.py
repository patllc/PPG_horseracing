from contextlib import closing
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import csv
import time
import datetime
import re

import sys

def main(matchdateurl,outputfile):
    ###Step 3 : open chrome driver, and locate the data table
    driver = webdriver.Chrome("YourPathtochromedriver")
    driver.set_page_load_timeout(30)

    rows=[]

    connected=False
    connected_trial=0
    while (not connected) & (connected_trial<5): #add try and reconnect to avoid server slow response
        connected_trial+=1
        #locate the data table
        try: # try and exception to avoid macro stops in batch run
            driver.get(matchdateurl)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table#All_Result_Table')))
            time.sleep(1)
            raw_html=driver.page_source
            connected=True
        except TimeoutException:
            raw_html = None
            time.sleep(3)
    ###
    
    #Step 2 : Store the table in list
    if raw_html is not None:
        data=[]
        try: # try and exception to avoid macro stops in batch run
            
            html = BeautifulSoup(raw_html,'html.parser',fromEncoding='utf-8')

            ###this section is very useful to obtain table format in html
            table_body = html.select('table#All_Result_Table')[0]
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols ])
            ###
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(e)
            print(exc_tb.tb_lineno)

        
        #Step 3: output to csv file (append)
        with open(outputfile, "a",newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
            time.sleep(1)

if __name__ == "__main__":
    main("https://race.netkeiba.com/race/result.html?race_id=201606050608&rf=race_list","output file path of EP3_result.csv")