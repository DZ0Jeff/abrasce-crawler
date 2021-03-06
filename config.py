from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setSelenium(console):
    # configuração do selenium 
    chrome_options = Options()
    if console:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    # evitar detecção anti-bot
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # desabilitar o log do chrome
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    return webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Selenium/chromedriver.exe",
                            service_log_path='NUL')

def init_crawler(URL):
    page = requests.get(URL)

    if page.status_code != 200:
        input(f'[ERRO {page.status_code}] Site indisponivel, tente novamente mais tarde')
        exit()

    crawler = BeautifulSoup(page.content,"html5lib")

    return crawler

def init_parser(html):
    return BeautifulSoup(html, "html5lib")