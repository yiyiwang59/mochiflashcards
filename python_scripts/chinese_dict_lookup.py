from pycccedict.cccedict import CcCedict
from pypinyin import pinyin, Style

class ChineseVocabLookup():
    def __init__(self):
        self.cccedict = CcCedict()
    #Lookup pinyin & english translation from one vocab word given
    def get_pinyin_translation(self, word):
        result = self.cccedict.get_entry(word)
        pinyin_word = self.format_pinyin_from_char(word)
        if result is not None:
            translation = "; ".join(result['definitions'])
            return pinyin_word, translation
        else: 
            return pinyin_word, "No translation found"

    #Format pinyin format with tone numbers to tone symbols
    def format_pinyin_from_char(self, char_input):
        converted = [x[0] for x in pinyin(char_input)]
        converted_pinyin = ' '.join(converted)
        return converted_pinyin

    #Full pinyin, english translation for a list of vocab words
    def lookup_vocab_list(self, vocab_list):
        full_list = []
        for vocab in vocab_list:
            if vocab != '':
                word_dict = {}
                lookup_pinyin, lookup_translation = self.get_pinyin_translation(vocab)
                word_dict['word'] = vocab
                word_dict['pinyin'] = lookup_pinyin
                word_dict['translation'] = lookup_translation
                full_list.append(word_dict)
            else:
                pass
        return full_list
            



