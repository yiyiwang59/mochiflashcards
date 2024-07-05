from pycccedict.cccedict import CcCedict
from pypinyin import pinyin, Style

def get_pinyin_translation(word):
    cccedict = CcCedict()
    result = cccedict.get_entry(word)
    pinyin_word = format_pinyin_from_char(word)
    if result is not None:
        translation = ", ".join(result['definitions'])
        return pinyin_word, translation
    else: 
        return pinyin_word, None

def format_pinyin_from_char(char_input):
    converted = [x[0] for x in pinyin(char_input)]
    converted_pinyin = ' '.join(converted)
    return converted_pinyin

def lookup_vocab_list(vocab_list):
    full_list = []
    for vocab in vocab_list:
        word_dict = {}
        lookup_pinyin, lookup_translation = get_pinyin_translation(vocab)
        word_dict['word'] = vocab
        word_dict['pinyin'] = lookup_pinyin
        word_dict['translation'] = lookup_translation
        full_list.append(word_dict)
    return full_list



