from pycccedict.cccedict import CcCedict
from pypinyin import pinyin, Style
import chinese_dict_lookup as ch
import airtable_API as at
import mochi_API as m
import airtable_mochi_sync as sync

at.fill_in_missing_data()
sync.sync_decks()
sync.sync_cards()

