from config import setSelenium, init_crawler,init_parser
from utils import JSONtoExcel, save_to_json, format_text
from current_time import *
from time import sleep
import string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException

global driver

def dynamic_html(url):
    driver = setSelenium(console=False)
    try:
        driver.get(url)
    
    except TimeoutException:
        print('Pagina não carregada...')
        return False

    sleep(10)
    results_div = driver.find_element_by_class_name('shopping-template-default')
    
    return results_div.get_attribute('outerHTML')


def load_button(url):
    driver = setSelenium()
    driver.get(url)

    
    try:
        for _ in range(0,6):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 1.5)")
            sleep(15)
            driver.find_element_by_id('loadMoreShopping').click()
            print('Mais shoppings encontrado!')
            if driver.find_element_by_id('loadMoreShopping').click():
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 1.4)")
                
        html = driver.find_element_by_tag_name('body')
        
        return html.get_attribute('outerHTML')    

    except NoSuchElementException:
        print('não tem mais shoppings!')
        html = driver.find_element_by_tag_name('body')
        
        return html.get_attribute('outerHTML')

    except ElementClickInterceptedException:
        print('Botão não localizado')
        html = driver.find_element_by_tag_name('body')
        
        return html.get_attribute('outerHTML')


def extract_shoppings(target_url):
    # Array que irá pegar todas informações extraídas
    data = []

    URL = target_url

    # Selenium
    html = load_button(URL)

    # Iniciar o crawler
    try:
        crawler = init_parser(html)
    except TypeError:
        print('pagina não encontrada')

    shoppings = crawler.find_all('div', id="ajax-content-shoppings")

    print('Localizando os links...')

    for shopping in shoppings:
        shopping_link = shopping.find_all('a')

        for link in shopping_link:
            # print(f"https://abrasce.com.br/{link['href']}")
            with open('links.txt', 'a') as file:
                file.write(f"{link['href']}\n")


        print(f'Finalizado! links extraidos!')

    print('Extração dos links completada...')


def read_link():
    print('Iniciando leitura de links...')
    with open('links.txt', 'r') as text:
        return text.readlines()


def extract_details():
    extracted_info = []

    print(f"{len(read_link())} links achados")

    contador = 1

    for shopping_page in read_link():
        print(f'Extraindo {contador} link')

        details = {}

        # inicializar drivers
        dynamic_result = dynamic_html(shopping_page)
        
        if dynamic_html == False:
            extracted_info.append(details)
            save_to_json(details)
            continue

        crawler = init_parser(dynamic_result)

        details['Nome'] = crawler.find('span', class_="post post-shopping current-item").text

        details['Tipo'] = crawler.find('a', class_="taxonomy operacao").text

        details['link'] = shopping_page

        details_container = crawler.find('div',class_="specs")

        # PERFIL DE CONSUMIDORES
        perfil_title = details_container.find(text="PERFIL DE CONSUMIDORES")
        class_content = perfil_title.findNext('div')

        class_perfil = []
        for p in class_content.find_all('p'):
            class_perfil.append(p.text)


        details['Classe A'] = class_perfil[0]
        details['Classe B'] = class_perfil[1]
        details['Classe C'] = class_perfil[2]
        details['Classe D'] = class_perfil[3]
        # details[perfil_title] = format_text(class_content.text)

        # ENTRETENIMENTO
        enterteiment_title = details_container.find(text="ENTRETENIMENTO")
        enterteiment_content = enterteiment_title.findNext('div')

        # print(enterteiment_title)
        details[enterteiment_title] = format_text(enterteiment_content.text)

        # ÁREA TOTAL DO TERRENO
        area_title = details_container.find(text="ÁREA TOTAL DO TERRENO")
        area_content = area_title.findNext('div')

        # print(area_title)
        details[area_title] = format_text(area_content.text)

        # CONTATO
        contact_title = details_container.find(text="CONTATO")
        contact_content = contact_title.findNext('ul')

        # print(contact_title)
        details[contact_title] = format_text(contact_content.text)

        # Icones

        aditional_info = crawler.find('div', class_="icons shoppings mt-4 mb-4")

        box = aditional_info.find_all('div', class_="box") 

        for box_info in box:
            title = box_info.find('p', class_='mb-0')
            detail_content = box_info.find('p', class_="number")
            
            details[title.text] = detail_content.text


        extracted_info.append(details)
        contador += 1
    
    save_to_json(details)

    print('Finalizado!')

    print('Salvando em json...')

    save_to_json(extracted_info)
    print('Finalizado...')


def main():
    # for page in string.ascii_uppercase:
    #     extract_shoppings(f"https://abrasce.com.br/guia-de-shoppings/?letter={page}")
    
    # extract_shoppings("https://abrasce.com.br/guia-de-shoppings/strip-mall/",)
    # extract_shoppings("https://abrasce.com.br/guia-de-shoppings/outlet-center/")

    extract_details()
    JSONtoExcel()


if __name__ == "__main__":
    start = timeit.default_timer()

    try:
        main()

        tempo_estimado(start)

    except KeyboardInterrupt:
        tempo_estimado(start)

    except Exception as error:
        tempo_estimado(start)
        raise
