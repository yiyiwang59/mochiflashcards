import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the path to python_scripts directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_scripts/')))

from python_scripts.chinese_dict_lookup import ChineseVocabLookup

class TestChineseVocabLookup(unittest.TestCase):

    @patch('chinese_dict_lookup.CcCedict')
    def setUp(self, MockCcCedict):
        self.mock_cccdict = MockCcCedict.return_value
        self.vocab_lookup = ChineseVocabLookup()

    def test_get_pinyin_translation(self):
        self.mock_cccdict.get_entry.return_value = {'definitions': 'shih tzu (dog breed)'}
        pinyin, translation = self.vocab_lookup.get_pinyin_translation('西施犬')
        self.assertEqual(pinyin, 'xī shī quǎn')
        self.assertEqual(translation, 'shih tzu (dog breed)')
    
    def test_format_pinyin_from_char(self):
        pinyin = self.vocab_lookup.format_pinyin_from_char('西施犬')
        self.assertEqual(pinyin, 'xī shī quǎn')

    def test_lookup_vocab_list(self):
        self.mock_cccdict.get_entry.return_value = {'definitions': 'shih tzu (dog breed)'}
        vocab_list = ['西施犬', '勇敢', '虎斑', '']
        result = self.vocab_lookup.lookup_vocab_list(vocab_list)
        expected = [{'word': '西施犬', 'pinyin': 'xī shī quǎn', 'translation': 'shih tzu (dog breed)'}, {'word': '勇敢', 'pinyin': 'yǒng gǎn', 'translation': 'brave;  courageous'}, {'word': '虎斑', 'pinyin': 'hǔ bān', 'translation': 'No translation found'}]
        self.assertEqual(result, expected)
    
    if __name__ == '__main__':
        unittest.main()

