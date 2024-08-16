from python_scripts.airtable_API import ConnectAirtableAPI
from python_scripts.mochi_API import MochiAPI

class AirtableMochiSync:
    def __init__(self):
        self.at = ConnectAirtableAPI()
        self.m = MochiAPI()
    #create mochi decks from airtable chinese lessons
    def sync_decks(self):
        at_decks_to_create = self.at.get_decks_to_create()
        for deck in at_decks_to_create:
            deck_name = deck['name']
            at_id = deck['id']
            parent_deck_id = self.m.get_deck_id(deck['type'])
            if deck['type'] != '' and parent_deck_id == None:
                parent_deck_id = self.m.create_deck(deck['type'])
            mochi_deck_id = self.m.create_deck(deck_name, parent_deck_id)
            #english_deck_id = m.create_deck('English First', mochi_deck_id)
            #chinese_deck_id = m.create_deck('Chinese First', mochi_deck_id)
            self.at.populate_mochi_id_lesson(at_id, mochi_deck_id)
            

    #create mochi cards from airtable chinese vocab
    def sync_cards(self):
        at_cards_to_create = self.at.get_cards_to_create()
        for card in at_cards_to_create:
            at_vocab_id = card['id']
            chinese = card['vocab']
            english = card['english']
            pinyin = card['pinyin']
            deck_id = self.m.get_deck_id(card['deck'])
            mochi_card_id_ch = self.m.create_card_chinese(chinese, english, pinyin, deck_id)
            mochi_card_id_eng = self.m.create_card_english(chinese, english, pinyin, deck_id)
            self.at.populate_mochi_id_vocab(at_vocab_id, mochi_card_id_ch, mochi_card_id_eng)

    #General AT to Mochi Sync (existing updates)

    #General Mochi to AT Sync (existing updates)