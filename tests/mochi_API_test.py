import unittest
import pytest
from unittest.mock import patch, MagicMock
from requests.auth import HTTPBasicAuth
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_scripts/')))

from python_scripts.mochi_API import MochiAPI

class TestMochiAPI(unittest.TestCase):
    @patch.dict(os.environ, {
    'MOCHI_API_TOKEN': 'fake_mochi_api_key',
    'MOCHI_TEMPLATE_CHINESE': 'fake_mochi_template_ch',
    'MOCHI_TEMPLATE_CHINESE_FIELD_ENG': 'fake_mochi_field_ch_eng',
    'MOCHI_TEMPLATE_CHINESE_FIELD_CH': 'fake_mochi_field_ch_ch',
    'MOCHI_TEMPLATE_CHINESE_FIELD_PY': 'fake_mochi_field_ch_py',
    'MOCHI_TEMPLATE_ENGLISH_ID': 'fake_mochi_template_eng',
    'MOCHI_TEMPLATE_ENGLISH_FIELD_ENG': 'fake_mochi_field_eng_eng',
    'MOCHI_TEMPLATE_ENGLISH_FIELD_CH': 'fake_mochi_field_eng_ch',
    'MOCHI_TEMPLATE_ENGLISH_FIELD_PY': 'fake_mochi_field_eng_py',
})
    def setUp(self):
        self.manager = MochiAPI()
    
    @patch('requests.post')
    def test_create_deck(self, mock_post):
        mock_post.return_value.json.return_value = {'id': '123'}
        deck_id = self.manager.create_deck('Test Deck')
        mock_post.assert_called_once_with(
            'https://app.mochi.cards/api/decks',
            json={'name': 'Test Deck'},
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth('fake_mochi_api_key', '')
            )
        self.assertEqual(deck_id, '123')

    @patch('requests.post')
    def test_create_card_chinese(self, mock_post):
        mock_post.return_value.json.return_value = {'id': 'abc'}
        card_id = self.manager.create_card_chinese('虎斑', 'tabby', 'hú bān', '123')
        mock_post.assert_called_once_with(
            'https://app.mochi.cards/api/cards/',
            json = {
            'content': '',
            'deck-id': '123',
            'template-id': 'fake_mochi_template_ch',
            'fields': {
                'name': {
                    'id': 'fake_mochi_field_ch_ch',
                    'value': '虎斑'
                },
                'fake_mochi_field_ch_eng': {
                    'id': 'fake_mochi_field_ch_eng',
                    'value': 'tabby'
                },
                'fake_mochi_field_ch_py': {
                    'id': 'fake_mochi_field_ch_py',
                    'value': 'hú bān'
                }
            }
        },
        headers={
            'Content-Type': 'application/json'
        },
        auth=HTTPBasicAuth('fake_mochi_api_key', '')
        )

        self.assertEqual(card_id, 'abc')
    
    @patch('requests.post')
    def test_create_card_english(self, mock_post):
        mock_post.return_value.json.return_value = {'id': 'abc'}
        card_id = self.manager.create_card_english('虎斑', 'tabby', 'hú bān', '123')
        mock_post.assert_called_once_with(
            'https://app.mochi.cards/api/cards/',
            json = {
            'content': '',
            'deck-id': '123',
            'template-id': 'fake_mochi_template_eng',
            'fields': {
                'name': {
                    'id': 'fake_mochi_field_eng_eng',
                    'value': 'tabby'
                },
                'fake_mochi_field_eng_ch': {
                    'id': 'fake_mochi_field_eng_ch',
                    'value': '虎斑'
                },
                'fake_mochi_field_eng_py': {
                    'id': 'fake_mochi_field_eng_py',
                    'value': 'hú bān'
                }
            }
        },
        headers={
            'Content-Type': 'application/json'
        },
        auth=HTTPBasicAuth('fake_mochi_api_key', '')
        )

        self.assertEqual(card_id, 'abc')

    @patch('requests.get')
    def test_get_cards(self, mock_get):
        mock_get.return_value.json.return_value = ({
            'tags': [], 
            'content': '', 
            'name': 'tabby', 
            'deck-id': '1234', 
            'fields': {
                'name': {
                    'id': 'name', 
                    'value': 'tabby'
                    }, 
                'fake_mochi_field_eng_py': {
                    'id': 'fake_mochi_field_eng_py', 
                    'value': 'hú bān'
                    }, 
                'fake_mochi_field_eng_ch': {
                    'id': 'fake_mochi_field_eng_ch', 
                    'value': '虎斑'
                    },
                'id': 'abcde',
                'template-id': 'fake_mochi_template_eng'
                }
            }, {
            'tags': [], 
            'content': '', 
            'name': '西施犬', 
            'deck-id': '1235', 
            'fields': {
                'name': {
                    'id': 'name', 
                    'value': '西施犬'
                    }, 
                'fake_mochi_field_ch_eng': {
                    'id': 'fake_mochi_field_ch_eng', 
                    'value': 'shih-tzu'
                    }, 
                'fake_mochi_field_ch_py': {
                    'id': 'fake_mochi_field_ch_py', 
                    'value': 'xī shī quán'
                    },
                'id': 'abcdf',
                'template-id': 'fake_mochi_template_ch'
                }
            }
        )
        expected = [{'mochi_id': 'abcde', 'chinese': '虎斑', 'pinyin': 'hú bān', 'english': 'tabby', 'mochi_deck_id': '1234'}, {'mochi_id': 'abcdf', 'chinese': '西施犬', 'pinyin': 'xī shī quán', 'english': 'shih-tzu', 'mochi_deck_id': '1235'}]
        result = self.manager.get_cards()
        mock_get.assert_called_once_with(
            'https://app.mochi.cards/api/cards/',
            headers={
            'Content-Type': 'application/json'
            },
            auth=HTTPBasicAuth('fake_mochi_api_key', '')
        )
        self.assertEqual(result, expected)

    @patch('requests.get')
    def test_get_all_decks(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.side_effect = [{
                'bookmark': 'bookmark1',
                'docs': [
                    {
                        'name': 'Fitness',
                        'id': '1234',
                    },
                    {
                        'name': 'Songs',
                        'id': '1235'
                    }
                ]
            },
            {
                'bookmark': 'bookmark2',
                'docs': [
                    {
                        'name': 'Textbook',
                        'id': '1236',
                    },
                    {
                        'name': 'Pets',
                        'id': '1237'
                    },
                    {
                        'name': 'Taylor Swift',
                        'id': '1238',
                    },
                    {
                        'name': 'Career',
                        'id': '1239'
                    }
                ]
            },
            {
                'bookmark': 'bookmark2',
                'docs': []
            }
        ]
        mock_get.return_value = mock_response
        result = self.manager.get_all_decks()
        expected = [{'mochi_id': '1234', 'name': 'Fitness'}, {'mochi_id': '1235', 'name': 'Songs'}, {'mochi_id': '1236', 'name': 'Textbook'}, {'mochi_id': '1237', 'name': 'Pets'}, {'mochi_id': '1238', 'name': 'Taylor Swift'}, {'mochi_id': '1239', 'name': 'Career'}]
        self.assertEqual(mock_get.call_count, 3)
        expected_url = 'https://app.mochi.cards/api/decks'
        calls = [
            unittest.mock.call(f'{expected_url}/', headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('fake_mochi_api_key', '')), unittest.mock.call().json,
            unittest.mock.call(f'{expected_url}?bookmark=bookmark1', headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('fake_mochi_api_key', '')), unittest.mock.call().json,
            unittest.mock.call(f'{expected_url}?bookmark=bookmark2', headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('fake_mochi_api_key', '')), unittest.mock.call().json,
        ]
        mock_get.assert_has_calls(calls, any_order=False)
        self.assertEqual(result, expected)

    @patch('python_scripts.mochi_API.MochiAPI.get_all_decks')
    def test_get_deck_id(self, mock_get_all_decks):
        mock_get_all_decks.return_value = [{'mochi_id': '1234', 'name': 'Fitness'}, {'mochi_id': '1235', 'name': 'Songs'}, {'mochi_id': '1236', 'name': 'Textbook'}, {'mochi_id': '1237', 'name': 'Pets'}, {'mochi_id': '1238', 'name': 'Taylor Swift'}, {'mochi_id': '1239', 'name': 'Career'}]
        test_Taylor_Swift = self.manager.get_deck_id('Taylor Swift')
        expected = '1238'
        self.assertEqual(test_Taylor_Swift, expected)
        test_none = self.manager.get_deck_id('Relationships')
        self.assertEqual(test_none, None)

if __name__ == '__main__':
    unittest.main()