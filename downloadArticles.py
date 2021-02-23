from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import stdiomask

usernameStr = input("Enter your UCF username: ")
passwordStr = stdiomask.getpass(prompt='Enter your UCF password: ')

companies = ["American Express Co", "Amgen Inc", "Apple Inc", "Boeing Co", "Caterpillar Inc", "Cisco Systems Inc", "Chevron Corp", "Goldman Sachs Group Inc", "Home Depot Inc", "Honeywell International Inc", "International Business Machines Corp", "Intel Corp", "Johnson & Johnson", "Coca-Cola Co", "JPMorgan Chase & Co", "McDonald’s Corp", "3M Co", "Merck & Co Inc", "Microsoft Corp", "Nike Inc", "Procter & Gamble Co", "Travelers Companies Inc", "UnitedHealth Group Inc", "Salesforce.Com Inc", "Verizon Communications Inc", "Visa Inc", "Walgreens Boots Alliance Inc", "Walmart Inc", "Walt Disney Co", "Dow Inc"]


# get the driver started
browser = webdriver.Chrome(executable_path='/Users/George/Documents/sentiment analyzer/chromedriver')
sleep = 3

def logIn(username, password, browser):

    # open nexis link
    browser.get('https://guides.ucf.edu/nexis')
    browser.find_element_by_xpath("//a[@href='https://guides.ucf.edu/database/LNA']").click()

    # login to nexis
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'userNameInput'))).send_keys(username)
    browser.find_element_by_id('passwordInput').send_keys(password)
    browser.find_element_by_id('submitButton').click()

def searchForCompany(companyName, browser):

    dateFilter = ['//*[@id="selectDateFilterOption"]/option[7]', '/html/body/main/div/div[13]/div[2]/div[1]/header/div[5]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div[2]/button', '//*[@id="datepicker"]/button[1]', '//*[@id="datepicker"]/table/tbody/tr[1]/td[6]/button', '/html/body/main/div/div[13]/div[2]/div[1]/header/div[5]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div[2]/div/div[2]/button', '//*[@id="datepicker"]/button[1]', '//*[@id="datepicker"]/table/tbody/tr[6]/td[1]/button', '//*[@id="zf_gkhk"]/div/div/div[2]/div[3]/div[2]/div/button']

    filters = ['//button[@data-filtertype="publicationtype"]', '//button[@data-filtertype="language"]', '//button[@data-filtertype="en-geography-news"]', '//button[@data-filtertype="en-subject"]']

    values = ['//label/span[contains(text(), "Newspapers")]', '//label/span[contains(text(), "English")]', '//label/span[contains(text(), "North America")]', '//label/span[contains(text(), "Business News")]']

    download = ['//input[@data-action="selectall"]', '//button[@data-action="downloadopt"]', '//input[@id="Rtf"]', '//input[@id="FileName"]', '//button[@type="submit"]']

    # type in the name of the company
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div[13]/div[2]/div[1]/header/div[5]/div/div/div[2]/div[2]/div/div[1]/div/div/div[3]/div/input"))).send_keys(companyName)

    # date filter and search
    for steps in dateFilter:
        browser.find_element_by_xpath(steps).click()
    time.sleep(1)

    # apply filters
    for path, value in zip(filters, values):
        try:
            browser.find_element_by_xpath(path).click()
            time.sleep(sleep)
            try:
                browser.find_element_by_xpath(value).click()
                time.sleep(sleep)
            except:
                browser.find_element_by_xpath('//button[contains(text(), "More")]').click()
                browser.find_element_by_xpath(value).click()
                time.sleep(sleep)
        except:
            continue;
    time.sleep(1)

    # download
    for step in download:
        if step == '//input[@id="Rtf"]':
            time.sleep(3)
        browser.find_element_by_xpath(step).click()
        if step == '//input[@id="FileName"]':
            ActionChains(browser).key_down(Keys.COMMAND).send_keys("a").key_up(Keys.COMMAND).key_down(Keys.BACKSPACE).perform()
            browser.find_element_by_xpath(step).send_keys(companyName)
    time.sleep(8)
    browser.find_element_by_xpath('//*[@id="nav_currentproduct_button"]').click()


logIn(usernameStr, passwordStr, browser)

for name in companies:
    searchForCompany(name, browser)
