from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from time import sleep
import EP1_settings

###Linkage to Statistic Model and Odds Monitoring System
# Build in the future
curr_raceno = 10
WIN_BET = [[1,100]]
QPL_BET = [['1-4',200]]

###

### Step 1 Open Browser and Load HKJC Website
chromedriver_path = EP1_settings.chromedriver_path
driver = webdriver.Chrome(chromedriver_path)

#maximize window
driver.maximize_window()

#load website
driver.get('https://bet.hkjc.com/default.aspx?url=/racing/pages/odds_wpq.aspx&lang=ch&dv=local')

#wait until account and password input box appears in the website
sleep(0.5)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#passwordInput1.accInfoInputField')))
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#account.accInfoInputField')))
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#loginButton')))

#type username and password
sleep(0.5)
acctbox=driver.find_element_by_css_selector('input#account.accInfoInputField')
ActionChains(driver).move_to_element(acctbox).click().send_keys(EP1_settings.hkjc_username).perform()
sleep(0.5)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#passwordInput1')))
pwbox=driver.find_element_by_css_selector('input#passwordInput1')
ActionChains(driver).move_to_element(pwbox).click().send_keys(EP1_settings.hkjc_password).perform()
sleep(0.5)

#click login button
sleep(0.5)
webloginbtn=driver.find_element_by_css_selector('div#loginButton')
webloginbtn.click()

#wait until the secret question popup appears
sleep(0.5)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#ekbaSeqQuestion'))) #span#ekbaSeqQuestion

#answer based on what secret question is
securityquestion=driver.find_element_by_css_selector('div#ekbaSeqQuestion').text
if securityquestion == EP1_settings.securityquestion1:
    securityanswer_text=EP1_settings.securityanswer_text1
elif securityquestion == EP1_settings.securityquestion2:
    securityanswer_text=EP1_settings.securityanswer_text2
else:
    securityanswer_text=EP1_settings.securityanswer_text3
securityanswer=driver.find_element_by_css_selector('input#ekbaDivInput.text')
ActionChains(driver).move_to_element(securityanswer).click().send_keys(securityanswer_text).send_keys(Keys.RETURN).perform()

#click disclaimer and confirm
sleep(0.5)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#disclaimerProceed')))
disclaimerbtn=driver.find_element_by_css_selector('div#disclaimerProceed')
disclaimerbtn.click()

#switch to current match
sleep(0.5)
driver.switch_to.default_content()
driver.find_element_by_xpath('//div[contains(@onclick, "selectRace(' + str(curr_raceno) + ')")]').click()

#place win bets
sleep(1)
driver.switch_to.default_content()
for horseid, betsize in WIN_BET:
    driver.find_element_by_xpath('//a[contains(@href, "WIN") and contains(@href, "' + str(horseid) + ')' + '")]').click()

#place QPL bets
for horseid, betsize in QPL_BET:
    driver.find_element_by_xpath('//a[contains(@href, "QPL") and contains(@href, "' + str(horseid) +'")]').click()

#change bet size for win bets
bet_cnt = 0
for horseid, betsize in WIN_BET:
    inputAmount=driver.find_element_by_xpath('//input[contains(@id, "inputAmount'+ str(int(bet_cnt)) + '")]')
    inputAmount.clear()
    ActionChains(driver).move_to_element(inputAmount).click().send_keys(int(betsize)).perform()
    bet_cnt += 1

#change bet size for qpl bets
for horseid, betsize in QPL_BET:
    inputAmount=driver.find_element_by_xpath('//input[contains(@id, "inputAmount'+ str(int(bet_cnt)) +'")]')
    inputAmount.clear()
    ActionChains(driver).move_to_element(inputAmount).click().send_keys(int(betsize)).perform()
    bet_cnt += 1

#click preview button
WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#bsSendPreviewButton')))
previewbtn=driver.find_element_by_id('bsSendPreviewButton')
previewbtn.click()