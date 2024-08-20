#from pycccedict.cccedict import CcCedict
#from pypinyin import pinyin, Style
from python_scripts.airtable_API import ConnectAirtableAPI
#from python_scripts.mochi_API import MochiAPI
from python_scripts.airtable_mochi_sync import AirtableMochiSync

vocab_lookup = ConnectAirtableAPI()
vocab_lookup.fill_in_missing_data()
sync = AirtableMochiSync()
sync.sync_decks()
sync.sync_cards()


