from pyairtable import Api, formulas
from dotenv import load_dotenv
import os
import chinese_dict_lookup as ch

# Load environment variables from .env file
load_dotenv()

# Access the variables
airtable_api_key = os.getenv('AIRTABLE_API_TOKEN')
base_id = os.getenv('AIRTABLE_BASE_ID')
table_name = os.getenv('AIRTABLE_TABLE_NAME')
english_translation = os.getenv('AIRTABLE_ENGLISH_TRANSLATION_ID')
english_translation_ref = formulas.FIELD(f'{english_translation}')
ch_vocab_field = os.getenv('AIRTABLE_CH_VOCAB_ID')
pinyin_field = os.getenv('AIRTABLE_PINYIN_ID')




api = Api(airtable_api_key)
table = api.table(base_id, table_name)

def get_missing_translation_records():
    airtable_json = table.all(fields=[f'{ch_vocab_field}'],formula=f"NOT({english_translation_ref})")
    output = []
    for record in airtable_json:
        record_dict = {}
        record_dict['id'] = record['id']
        record_dict['vocab_word'] = record['fields']['Name'].strip()
        output.append(record_dict)
    return output

def fill_in_missing_data():
    records = get_missing_translation_records()
    complete_output = []
    for line in records:
        record_dict = {}
        fields_dict = {}
        pinyin_lookup, translation_lookup = ch.get_pinyin_translation(line['vocab_word'])
        record_dict['id'] = line['id']
        fields_dict[f'{ch_vocab_field}'] = line['vocab_word']
        fields_dict[f'{pinyin_field}'] = pinyin_lookup
        fields_dict[f'{english_translation}'] = translation_lookup
        record_dict['fields'] = fields_dict
        complete_output.append(record_dict)
    parse_for_airtable(complete_output)


def parse_for_airtable(data):
    table.batch_update(data)


    
    
