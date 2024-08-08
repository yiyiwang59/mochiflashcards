import unittest
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_scripts/')))

from python_scripts.airtable_API import ConnectAirtableAPI

class TestConnectAirtableAPI(unittest.TestCase):
    @patch.dict(os.environ, {
        'AIRTABLE_API_TOKEN': 'fake_api_token',
        'AIRTABLE_BASE_ID': 'fake_base_id',
        'AIRTABLE_VOCAB_TABLE_ID': 'fake_vocab_table_id',
        'AIRTABLE_LESSON_TABLE_ID': 'fake_lesson_table_id',
        'AIRTABLE_ENGLISH_TRANSLATION_ID': 'fake_english_translation_id',
        'AIRTABLE_CH_VOCAB_ID': 'fake_ch_vocab_id',
        'AIRTABLE_PINYIN_ID': 'fake_pinyin_id',
        'AIRTABLE_LESSON_NAME_ID': 'fake_lesson_name_id',
        'AIRTABLE_LESSON_TYPE_ID': 'fake_lesson_type_id',
        'AIRTABLE_MOCHI_DECK_ID': 'fake_mochi_deck_id',
        'AIRTABLE_MOCHI_CARD_CH_ID': 'fake_mochi_card_ch_id',
        'AIRTABLE_MOCHI_CARD_ENG_ID': 'fake_mochi_card_eng_id'
    })
    def setUp(self):
            self.manager = ConnectAirtableAPI()
    
    def test_get_missing_translation_records(self):
        with patch.object(self.manager.vocab_table, 'all', return_value = [
            {'id': 'rec1', 'fields': {'Name': '词1'}},
            {'id': 'rec2', 'fields': {'Name': '词2'}}

        ]):
            records = self.manager.get_missing_translation_records()
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]['id'], 'rec1')
            self.assertEqual(records[0]['vocab_word'], '词1')
    
    if __name__ == '__main__':
         unittest.main()



        



