import requests
import json
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

class MochiAPI():
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Access the Mochi API key
        self.mochi_api_key = os.getenv('MOCHI_API_TOKEN')
        self.mochi_template_ch = os.getenv('MOCHI_TEMPLATE_CHINESE')
        self.mochi_field_ch_eng = os.getenv('MOCHI_TEMPLATE_CHINESE_FIELD_ENG')
        self.mochi_field_ch_ch = os.getenv('MOCHI_TEMPLATE_CHINESE_FIELD_CH')
        self.mochi_field_ch_py = os.getenv('MOCHI_TEMPLATE_CHINESE_FIELD_PY')
        self.mochi_template_eng = os.getenv('MOCHI_TEMPLATE_ENGLISH_ID')
        self.mochi_field_eng_eng = os.getenv('MOCHI_TEMPLATE_ENGLISH_FIELD_ENG')
        self.mochi_field_eng_ch = os.getenv('MOCHI_TEMPLATE_ENGLISH_FIELD_CH')
        self.mochi_field_eng_py = os.getenv('MOCHI_TEMPLATE_ENGLISH_FIELD_PY')

    #Create a new deck
    def create_deck(self, name, parent_deck_id=None):
        url = 'https://app.mochi.cards/api/decks'
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "name": name
        }
        if parent_deck_id is not None:
            payload['parent-id'] = parent_deck_id
        response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(self.mochi_api_key, ''))
        return response.json()['id']

    #Create a card with Chinese first template
    def create_card_chinese(self, chinese, english, pinyin, deck):
        url =  'https://app.mochi.cards/api/cards/'
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            'content': '',
            'deck-id': f'{deck}',
            'template-id': self.mochi_template_ch,
            'fields':{
                'name': {
                    'id': self.mochi_field_ch_ch,
                    'value': chinese
                },
                self.mochi_field_ch_eng: {
                    'id': self.mochi_field_ch_eng,
                    'value': english
                },
                self.mochi_field_ch_py: {
                    'id': self.mochi_field_ch_py,
                    'value': pinyin
                }
            } 
        }
        response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(self.mochi_api_key, ''))
        return response.json()['id']

    #Create card with English first template
    def create_card_english(self, chinese, english, pinyin, deck):
        url =  'https://app.mochi.cards/api/cards/'
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            'content': '',
            'deck-id': f'{deck}',
            'template-id': self.mochi_template_eng,
            'fields':{
                'name': {
                    'id': self.mochi_field_eng_eng,
                    'value': english
                },
                self.mochi_field_eng_ch: {
                    'id': self.mochi_field_eng_ch,
                    'value': chinese
                },
                self.mochi_field_eng_py: {
                    'id': self.mochi_field_eng_py,
                    'value': pinyin
                }
            } 
        }
        response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(self.mochi_api_key, ''))
        return response.json()['id']

    #Create card with Vocab Quiz Template


    #Get all cards
    def get_cards(self, deck_id=None):
        url = 'https://app.mochi.cards/api/cards/'
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(self.mochi_api_key, ''))
        result = []
        for card in response.json():
            word = {}
            word['mochi_id'] = card['fields']['id']
            if card['fields']['template-id'] == self.mochi_template_eng:
                word['chinese'] = card['fields'][f'{self.mochi_field_eng_ch}']['value']
                word['pinyin'] = card['fields'][f'{self.mochi_field_eng_py}']['value']
                word['english'] = card['name']
                word['mochi_deck_id'] = card['deck-id']
            elif card['fields']['template-id'] == self.mochi_template_ch:
                word['chinese'] = card['name']
                word['pinyin'] = card['fields'][f'{self.mochi_field_ch_py}']['value']
                word['english'] = card['fields'][f'{self.mochi_field_ch_eng}']['value']
                word['mochi_deck_id'] = card['deck-id']
            result.append(word)
        return result


    #get all decks
    def get_all_decks(self):
        url = 'https://app.mochi.cards/api/decks/'
        headers = {
            "Content-Type": "application/json"
        }
        response_json_full = []
        bookmark = None
        while True:
            if bookmark is not None:
                url = f'https://app.mochi.cards/api/decks?bookmark={bookmark}'
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth(self.mochi_api_key, ''))
            response_json = response.json()
            bookmark = response_json['bookmark']
            if len(response_json['docs']) == 0:
                break
            response_json_full.append(response_json)
            
        output = []
        for page in response_json_full:
            for item in page['docs']:
                item_dict = {}
                item_dict['mochi_id'] = item['id']
                item_dict['name'] = item['name']
                output.append(item_dict)
        return output


    #get deck id from name
    def get_deck_id(self, deck_name):
        all_decks = self.get_all_decks()
        lookup_deck_id = ''
        for deck in all_decks:
            print(deck)
            if deck_name == deck['name']:
                lookup_deck_id = deck['mochi_id']
                break
            else:
                continue
        if lookup_deck_id != '':
            return lookup_deck_id
        else:
            return None
