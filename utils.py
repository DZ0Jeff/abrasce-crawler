import json
import pandas as pd


def JSONtoExcel():
    print('Iniciando convensão...')
    
    df = pd.read_json('shoppings.json')
    df.to_excel('shoppings.xlsx')
    print('Convensão realizada com sucesso!')


def save_to_json(data):
    with open('shoppings.json','w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def format_text(text):
    return " ".join(text.split()).replace('\n','').replace('\r','').replace('\t','')