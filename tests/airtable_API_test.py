import unittest
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
            {'id': '1234', 'fields': {'Name': '友好'}},
            {'id': '1235', 'fields': {'Name': '虎斑'}},
        ]):
            #This needs to test the API call that only gets records with null english translation
            records = self.manager.get_missing_translation_records()
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]['id'], '1234')
            self.assertEqual(records[0]['vocab_word'], '友好')
    
    @patch('python_scripts.airtable_API.ChineseVocabLookup.get_pinyin_translation')
    def test_fill_in_missing_data(self, mock_get_pinyin_translation):
        self.manager.vocab_table = MagicMock()
        self.manager.vocab_table.all.return_value = [
            {'id': '1234', 'fields': {'Name': '友好'}},
            {'id': '1235', 'fields': {'Name': '虎斑'}},
        ]

        mock_get_pinyin_translation.side_effect = [
             ('yǒu hǎo', 'friendly; amicable; close friend'),
             ('hǔ bān', 'tabby')
        ]

        self.manager.fill_in_missing_data()
        expected_update = [
             {
                  'id': '1234', 
                  'fields': {
                       'fake_ch_vocab_id': '友好',
                       'fake_pinyin_id': 'yǒu hǎo',
                       'fake_english_translation_id': 'friendly; amicable; close friend'
                  }
            },
            {
                 'id': '1235',
                 'fields': {
                      'fake_ch_vocab_id': '虎斑',
                      'fake_pinyin_id': 'hǔ bān',
                      'fake_english_translation_id': 'tabby'
                 }
            }
        ]
        self.manager.vocab_table.batch_update.assert_called_once_with(expected_update)            

    def test_get_decks_to_create(self):
        self.manager.lesson_table = MagicMock()
        self.manager.lesson_table.all.return_value = [
              {'id': '1234', 'fields': {'Name': 'Pets', 'Type': 'Conversation Topics'}},
              {'id': '1235', 'fields': {'Name': '体面', 'Type': 'Songs'}}
         ]
        expected = [
             {'id': '1234', 'name': 'Pets', 'type': 'Conversation Topics'},
             {'id': '1235', 'name': '体面', 'type': 'Songs'}
        ]
        result = self.manager.get_decks_to_create()
        self.assertEqual(result, expected)

    @patch('python_scripts.airtable_API.ConnectAirtableAPI.get_lesson_name')
    def test_get_cards_to_create(self, mock_get_lesson_name):
        self.manager.vocab_table = MagicMock()
        self.manager.vocab_table.all.return_value = [
             {
                  'id': '1234', 
                  'fields': {
                       'Name': '友好',
                       'Pinyin': 'yǒu hǎo',
                       'English Translation': 'friendly; amicable; close friend',
                       'Chinese Lesson': ('abcd',)
                  }
            },
            {
                 'id': '1235',
                 'fields': {
                      'Name': '虎斑',
                      'Pinyin': 'hǔ bān',
                      'English Translation': 'tabby',
                      'Chinese Lesson': ('abce',)
                 }
            }
        ]
        mock_get_lesson_name.side_effect = ['Pets', '体面']

        expected = [
             {'id': '1234', 'vocab': '友好', 'pinyin': 'yǒu hǎo', 'english': 'friendly; amicable; close friend', 'deck': 'Pets'},
             {'id': '1235', 'vocab': '虎斑', 'pinyin': 'hǔ bān', 'english': 'tabby', 'deck': '体面'}
        ]
        result = self.manager.get_cards_to_create()
        self.assertEqual(result, expected)
        
    def test_populate_mochi_id_lesson(self):
        self.manager.lesson_table = MagicMock()
        lesson_id = 'abcd'
        mochi_id = '9876'
        self.manager.populate_mochi_id_lesson(lesson_id, mochi_id)
        self.manager.lesson_table.update.assert_called_once_with(lesson_id, {'fake_mochi_deck_id': mochi_id})
         
    def test_populate_mochi_id_vocab(self):
         self.manager.vocab_table = MagicMock()
         vocab_id = '1234'
         mochi_id_ch = 'wxyz'
         mochi_id_eng = 'zyxw'
         self.manager.populate_mochi_id_vocab(vocab_id, mochi_id_ch, mochi_id_eng)
         self.manager.vocab_table.update.assert_called_once_with(vocab_id, {'fake_mochi_card_ch_id': mochi_id_ch, 'fake_mochi_card_eng_id': mochi_id_eng})
    
    def test_get_lesson_name(self):
        self.manager.lesson_table = MagicMock()
        self.manager.lesson_table.get.return_value = {
                   'id': 'abce',
                   'fields': {
                        'Name': '体面',
                        'Type': 'Songs'
                   }
              }
        result = self.manager.get_lesson_name('abce')
        expected = '体面'
        self.assertEqual(expected, result)


    if __name__ == '__main__':
         unittest.main()



        



