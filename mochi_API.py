import requests
import json
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

# Access the Mochi API key
mochi_api_key = os.getenv('MOCHI_API_TOKEN')
mochi_template_ch = os.getenv('MOCHI_TEMPLATE_CHINESE')
mochi_field_ch_eng = os.getenv('MOCHI_TEMPLATE_CHINESE_FIELD_ENG')
mochi_field_ch_ch = os.getenv('MOCHI_TEMPLATE_CHINESE_FIELD_CH')
mochi_field_ch_py = os.getenv('MOCHI_TEMPLATE_CHINESE_FIELD_PY')
mochi_template_eng = os.getenv('MOCHI_TEMPLATE_ENGLISH_ID')
mochi_field_eng_eng = os.getenv('MOCHI_TEMPLATE_ENGLISH_FIELD_ENG')
mochi_field_eng_ch = os.getenv('MOCHI_TEMPLATE_ENGLISH_FIELD_CH')
mochi_field_eng_py = os.getenv('MOCHI_TEMPLATE_ENGLISH_FIELD_PY')


def create_deck(name, parent_deck_id=None):
    url = 'https://app.mochi.cards/api/decks'
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": name
    }
    if parent_deck_id is not None:
        payload['parent-id'] = parent_deck_id
    response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(mochi_api_key, ''))
    return response.json()['id']

def create_card_chinese(chinese, english, pinyin, deck):
    url =  'https://app.mochi.cards/api/cards/'
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        'content': '',
        'deck-id': f'{deck}',
        'template-id': mochi_template_ch,
        'fields':{
            'name': {
                'id': mochi_field_ch_eng,
                'value': english
            },
            mochi_field_ch_eng: {
                'id': mochi_field_ch_eng,
                'value': english
            },
            mochi_field_eng_py: {
                'id': mochi_field_eng_py,
                'value': pinyin
            }
            
        } 
    }
    response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(mochi_api_key, ''))
    return response.json()['id']

def create_card_english(chinese, english, pinyin, deck):
    url =  'https://app.mochi.cards/api/cards/'
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        'content': '',
        'deck-id': f'{deck}',
        'template-id': mochi_template_eng,
        'fields':{
            'name': {
                'id': mochi_field_eng_ch,
                'value': chinese
            },
            mochi_field_eng_ch: {
                'id': mochi_field_eng_ch,
                'value': chinese
            },
            mochi_field_ch_py: {
                'id': mochi_field_ch_py,
                'value': pinyin
            }
            
        } 
    }
    response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(mochi_api_key, ''))
    return response.json()['id']

def get_cards(deck_id=None):
    url = 'https://app.mochi.cards/api/cards/'
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(mochi_api_key, ''))
    return response.json()