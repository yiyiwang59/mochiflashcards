import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_scripts/')))

from python_scripts.airtable_mochi_sync import AirtableMochiSync

class TestAirtableMochiSync(unittest.TestCase):
    def setUp(self):
        self.manager = AirtableMochiSync()
    
    @patch('python_scripts.airtable_mochi_sync.ConnectAirtableAPI.populate_mochi_id_lesson')
    @patch('python_scripts.airtable_mochi_sync.MochiAPI.create_deck')
    @patch('python_scripts.airtable_mochi_sync.MochiAPI.get_deck_id')
    @patch('python_scripts.airtable_mochi_sync.ConnectAirtableAPI.get_decks_to_create')
    def test_sync_decks(self, mock_get_decks_to_create, mock_get_deck_id, mock_create_deck, mock_populate_mochi_id_lesson):
        mock_get_decks_to_create.return_value = [
            {
                'id': '1234',
                'name': 'Pets',
                'type': 'Conversation Topics'
            },
            {
                'id': '1235',
                'name': 'Career',
                'type': 'Conversation Topics'
            },
            {
                'id': '1236',
                'name': '体面',
                'type': 'Songs'
            }
        ]
        mock_get_deck_id.side_effect = [None, 'abcdh', None]
        mock_create_deck.side_effect = ['abcdh', 'abcdf', 'abcde', 'abcdg', 'abcdi']
        result = self.manager.sync_decks()
        calls = [
            unittest.mock.call('1234', 'abcdf'),
            unittest.mock.call('1235', 'abcde'),
            unittest.mock.call('1236', 'abcdi')
        ]
        mock_populate_mochi_id_lesson.assert_has_calls(calls, False)
        self.assertEqual(mock_populate_mochi_id_lesson.call_count, 3)
    
    @patch('python_scripts.airtable_mochi_sync.ConnectAirtableAPI.populate_mochi_id_vocab')
    @patch('python_scripts.airtable_mochi_sync.MochiAPI.create_card_english')
    @patch('python_scripts.airtable_mochi_sync.MochiAPI.create_card_chinese')
    @patch('python_scripts.airtable_mochi_sync.MochiAPI.get_deck_id')
    @patch('python_scripts.airtable_mochi_sync.ConnectAirtableAPI.get_cards_to_create')
    def test_sync_cards(self, mock_get_cards_to_create, mock_get_deck_id, mock_create_card_chinese, mock_create_card_english, mock_populate_mochi_id_vocab):
        mock_get_cards_to_create.return_value = [
            {
                'id': '1234',
                'vocab': '友好',
                'pinyin': 'yǒu hǎo',
                'english': 'friendly; amicable; close friend', 
                'deck': 'Travel'
            },
            {
                'id': '1235',
                'vocab': '虎斑',
                'pinyin': 'hǔ bān',
                'english': 'tabby', 
                'deck': 'Pets'
            },
            {
                'id': '1236',
                'vocab': '西施犬',
                'pinyin': 'xī shī quǎn',
                'english': 'shih tzu (dog breed)', 
                'deck': 'Pets'
            }
        ]
        mock_get_deck_id.side_effect = ['abcde', 'abcdf', 'abcdf']
        mock_create_card_chinese.side_effect = ['98765', '98764', '98763']
        mock_create_card_english.side_effect = ['98762', '98761', '98760']
        self.manager.sync_cards()
        vocab_calls = [
            unittest.mock.call('友好', 'friendly; amicable; close friend', 'yǒu hǎo', 'abcde'),
            unittest.mock.call('虎斑', 'tabby', 'hǔ bān', 'abcdf'),
            unittest.mock.call('西施犬', 'shih tzu (dog breed)', 'xī shī quǎn', 'abcdf')
        ]
        mock_create_card_chinese.assert_has_calls(vocab_calls, False)
        mock_create_card_english.assert_has_calls(vocab_calls, False)
        id_calls = [
            unittest.mock.call('1234', '98765', '98762'),
            unittest.mock.call('1235', '98764', '98761'),
            unittest.mock.call('1236', '98763', '98760')
        ]
        mock_populate_mochi_id_vocab.assert_has_calls(id_calls, False)


if __name__ == '__main__':
    unittest.main()