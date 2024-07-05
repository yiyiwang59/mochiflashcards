from pyairtable import Api, formulas
from dotenv import load_dotenv
import os
import chinese_dict_lookup as ch

# Load environment variables from .env file
load_dotenv()

# Access the variables
airtable_api_key = os.getenv('AIRTABLE_API_TOKEN')
base_id = os.getenv('AIRTABLE_BASE_ID')
vocab_table_id = os.getenv('AIRTABLE_VOCAB_TABLE_ID')
lesson_table_id = os.getenv('AIRTABLE_LESSON_TABLE_ID')
english_translation = os.getenv('AIRTABLE_ENGLISH_TRANSLATION_ID')
english_translation_ref = formulas.FIELD(f'{english_translation}')
ch_vocab_field = os.getenv('AIRTABLE_CH_VOCAB_ID')
pinyin_field = os.getenv('AIRTABLE_PINYIN_ID')
lesson_name_id = os.getenv('AIRTABLE_LESSON_NAME_ID')
lesson_type_id = os.getenv('AIRTABLE_LESSON_TYPE_ID')
mochi_deck_id = os.getenv('AIRTABLE_MOCHI_DECK_ID')
mochi_deck_ref = formulas.FIELD(f'{mochi_deck_id}')
mochi_card_id = os.getenv('AIRTABLE_MOCHI_CARD_ID')
mochi_card_ref = formulas.FIELD(f'{mochi_card_id}')


api = Api(airtable_api_key)
vocab_table = api.table(base_id, vocab_table_id)
lesson_table = api.table(base_id, lesson_table_id)

def get_missing_translation_records():
    airtable_json = vocab_table.all(fields=[f'{ch_vocab_field}'],formula=f"NOT({english_translation_ref})")
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
    vocab_table.batch_update(complete_output)


#get chinese lesson names with null mochi ID
def get_decks_to_create():
    airtable_json = lesson_table.all(fields=[f'{lesson_name_id}', f'{lesson_type_id}'],formula=f"NOT({mochi_deck_ref})")
    output = []
    for record in airtable_json:
        record_dict = {}
        record_dict['id'] = record['id']
        record_dict['name'] = record['fields']['Name'].strip()
        record_dict['type'] = record['fields']['Type']
        output.append(record_dict)
    return output

#get chinese vocab data with null mochi ID
def get_cards_to_create():
    airtable_json = vocab_table.all(formula=f"NOT({mochi_card_ref})")
    output = []
    for record in airtable_json:
        record_dict = {}
        record_dict['id'] = record['id']
        record_dict['vocab'] = record['fields']['Name'].strip()
        record_dict['pinyin'] = record['fields']['Pinyin']
        record_dict['english'] = record['fields']['English Translation']
        record_dict['deck'] = record['fields']['Chinese Lesson'][0]
        output.append(record_dict)
    return output

#populate mochi ID for chinese lesson
def populate_mochi_id_lesson(lesson_id, mochi_id):
    lesson_table.update(lesson_id, {f"{mochi_deck_id}": mochi_id})



#populate mochi ID for chinese vocab
    
