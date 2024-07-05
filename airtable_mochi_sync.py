import airtable_API as at
import mochi_API as m

#create mochi decks from airtable chinese lessons
def sync_decks():
    at_decks_to_create = at.get_decks_to_create()
    for deck in at_decks_to_create:
        deck_name = deck['name']
        at_id = deck['id']
        parent_deck_id = m.get_deck_id(deck['type'])
        if deck['type'] != '' and parent_deck_id == None:
            parent_deck_id = m.create_deck(deck['type'])
        mochi_deck_id = m.create_deck(deck_name, parent_deck_id)
        at.populate_mochi_id_lesson(at_id, mochi_deck_id)
        

#create mochi cards from airtable chinese vocab