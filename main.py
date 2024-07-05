from pycccedict.cccedict import CcCedict
from pypinyin import pinyin, Style
import chinese_dict_lookup as ch
import airtable_API as at

get_vocab = at.fill_in_missing_data()
print(get_vocab)

