from pyairtable import Api, formulas
from dotenv import load_dotenv
import os
from chinese_dict_lookup import ChineseVocabLookup

class ConnectAirtableAPI():
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Access the variables
        self.airtable_api_key = os.getenv('AIRTABLE_API_TOKEN')
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.vocab_table_id = os.getenv('AIRTABLE_VOCAB_TABLE_ID')
        self.lesson_table_id = os.getenv('AIRTABLE_LESSON_TABLE_ID')
        self.english_translation = os.getenv('AIRTABLE_ENGLISH_TRANSLATION_ID')
        self.ch_vocab_field = os.getenv('AIRTABLE_CH_VOCAB_ID')
        self.pinyin_field = os.getenv('AIRTABLE_PINYIN_ID')
        self.lesson_name_id = os.getenv('AIRTABLE_LESSON_NAME_ID')
        self.lesson_type_id = os.getenv('AIRTABLE_LESSON_TYPE_ID')
        self.mochi_deck_id = os.getenv('AIRTABLE_MOCHI_DECK_ID')
        self.mochi_card_id_ch = os.getenv('AIRTABLE_MOCHI_CARD_CH_ID')
        self.mochi_card_id_eng = os.getenv('AIRTABLE_MOCHI_CARD_ENG_ID')


        self.api = Api(self.airtable_api_key)
        self.vocab_table = self.api.table(self.base_id, self.vocab_table_id)
        self.lesson_table = self.api.table(self.base_id, self.lesson_table_id)

        self.english_translation_ref = formulas.FIELD(f'{self.english_translation}')
        self.mochi_deck_ref = formulas.FIELD(f'{self.mochi_deck_id}')
        self.mochi_card_ref = formulas.FIELD(f'{self.mochi_card_id_ch}')

        self.ch = ChineseVocabLookup()

    #Get any lines where english translation column is null
    def get_missing_translation_records(self):
        airtable_json = self.vocab_table.all(fields=[f'{self.ch_vocab_field}'],formula=f"NOT({self.english_translation_ref})")
        output = []
        for record in airtable_json:
            record_dict = {}
            record_dict['id'] = record['id']
            record_dict['vocab_word'] = record['fields']['Name'].strip()
            output.append(record_dict)
        return output

    #Fill in pinyin and english translation for all lines with english translation = null
    def fill_in_missing_data(self):
        records = self.get_missing_translation_records()
        complete_output = []
        for line in records:
            record_dict = {}
            fields_dict = {}
            pinyin_lookup, translation_lookup = self.ch.get_pinyin_translation(line['vocab_word'])
            record_dict['id'] = line['id']
            fields_dict[f'{self.ch_vocab_field}'] = line['vocab_word']
            fields_dict[f'{self.pinyin_field}'] = pinyin_lookup
            fields_dict[f'{self.english_translation}'] = translation_lookup
            record_dict['fields'] = fields_dict
            complete_output.append(record_dict)
        self.vocab_table.batch_update(complete_output)


    #get chinese lesson names with null mochi ID
    def get_decks_to_create(self):
        airtable_json = self.lesson_table.all(fields=[f'{self.lesson_name_id}', f'{self.lesson_type_id}'],formula=f"NOT({self.mochi_deck_ref})")
        output = []
        for record in airtable_json:
            record_dict = {}
            record_dict['id'] = record['id']
            record_dict['name'] = record['fields']['Name'].strip()
            record_dict['type'] = record['fields']['Type']
            output.append(record_dict)
        return output

    #get chinese vocab data with null mochi ID
    def get_cards_to_create(self):
        airtable_json = self.vocab_table.all(formula=f"NOT({self.mochi_card_ref})")
        output = []
        for record in airtable_json:
            record_dict = {}
            record_dict['id'] = record['id']
            record_dict['vocab'] = record['fields']['Name'].strip()
            record_dict['pinyin'] = record['fields']['Pinyin']
            record_dict['english'] = record['fields']['English Translation']
            record_dict['deck'] = self.get_lesson_name(record['fields']['Chinese Lesson'][0])
            output.append(record_dict)
        return output

    #populate mochi ID for chinese lesson
    def populate_mochi_id_lesson(self, lesson_id, mochi_id):
        self.lesson_table.update(lesson_id, {f"{self.mochi_deck_id}": mochi_id})

    #populate mochi ID for chinese vocab
    def populate_mochi_id_vocab(self, vocab_id, mochi_id_ch, mochi_id_eng):
        self.vocab_table.update(vocab_id, {f"{self.mochi_card_id_ch}": mochi_id_ch, f"{self.mochi_card_id_eng}": mochi_id_eng})
        
    #lookup chinese lesson name from ID
    def get_lesson_name(self, lesson_id):
        output = self.lesson_table.get(lesson_id)
        return output['fields']['Name']