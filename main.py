from pycccedict.cccedict import CcCedict
from pypinyin import pinyin, Style
import chinese_dict_lookup as ch
import airtable_API as at
import mochi_API as m
import airtable_mochi_sync as sync

sync.sync_decks()

