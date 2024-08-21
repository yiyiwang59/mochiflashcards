
---

# Testing Documentation

## Overview

This document provides detailed information on the unit tests written for the `mochiflashcards` project. Each test verifies the functionality of specific methods in the `AirtableMochiSync`, `AirtableAPI`, `ChineseVocabLookup` and `MochiAPI` classes. The purpose of these tests is to ensure that the integration between Airtable and Mochi Cards works as expected.

## Test Structure

The tests are organized using the `unittest` framework, with dependencies mocked using the `unittest.mock` library. This approach allows the isolation of the functions being tested and ensures that external API calls and environment variables do not interfere with the test results.

### Prerequisites

- Python 3.7+
- `unittest`
- `unittest.mock`
- `pytest` (if using pytest for running the tests)

---

## Testing Documentation
  
#### `airtable_API_test.py`

**Purpose:**
This test file is responsible for testing the `ConnectAirtableAPI` class methods. The tests focus on ensuring that the methods behave as expected when interacting with the Airtable API.

**Unit Tests:**
1. **`test_fill_in_missing_data`**
- **Description:** Tests the `fill_in_missing_data` method to ensure it correctly identifies and fills in any missing data from the Airtable records.
- **Mocked Dependencies:**
	- Airtable API's `get_pinyin_translation` function.
	- Airtable API's `vocab_table` property.
- **Assertions:**
	- Verify that the `get_pinyin_translation` function is called with the expected arguments.
	- Ensure that the Airtable record is updated with the correct translations.

2. **`test_get_cards_to_create`**
- **Description:** Tests the `get_cards_to_create` method to ensure it retrieves the correct set of cards that need to be created in Mochi.
- **Mocked Dependencies:**
	- Airtable API's `vocab_table` property.
- **Assertions:**
	- Ensure the method filters and returns the correct list of cards needing creation.
  
3. **`test_populate_mochi_id_vocab`**
- **Description:** Tests the `populate_mochi_id_vocab` method to ensure it properly updates the Airtable records with the generated Mochi card IDs.
- **Mocked Dependencies:**
	- Airtable API's `vocab_table` property.
- **Assertions:**
	- Verify that the Airtable record is updated with the correct Mochi card IDs.

4. `test_get_decks_to_create`
- **Description:** Tests the `get_decks_to_create` method to ensure it correctly retrieves and processes decks to create from Airtable.
- **Mocked Dependencies:**
	- Airtable API's `lesson_table` property
- **Assertions:**
	- Ensure the method filters and returns the correct list of decks to create

5. `test_get_missing_translation_records`
- **Description:** Tests the `get_missing_translation_records` method to ensure it correctly retrieves the correct rows from the `Chinese Vocab` table.
- **Mocked Dependencies:**
	- Airtable API's `vocab_table` property
- **Assertions:**
	- Ensure the method retrieves the correct filtered list of vocab words to lookup translations for
6. `test_populate_mochi_id_lesson`
- **Description:** Tests the `populate_mochi_id_lesson` method to ensure it properly updates the Airtable records with the generated Mochi Deck IDs.
- **Mocked Dependencies:**
	- Airtable API's `lesson_table` property
- **Assertions:**
	- Verify that the Airtable record is updated with the correct Mochi deck IDs.

7. `test_get_lesson_name`
- **Description:** Tests the `get_lesson_name` method to ensure it retrieves the correct lesson name from the id given
- **Mocked Dependencies:**
	- Airtable API's `lesson_table` property
- **Assertions:**
	- Verify that the lesson name returned is the correct for the id submitted

---
### `airtable_mochi_sync_test.py`
**Purpose:**
This test file is responsible for testing the `AirtableMochiSync` class methods. The tests focus on ensuring that the synchronization logic between Airtable and Mochi works correctly.

**Unit Tests:**
1. **`test_sync_decks`**
- **Description:** Tests the `sync_decks` method to ensure it correctly synchronizes the deck structure between Airtable and Mochi.
- **Mocked Dependencies:**
	- `ConnectAirtableAPI.get_decks_to_create`
	- `MochiAPI.get_deck_id`
	- `MochiAPI.create_deck`
	- `ConnectAirtableAPI.populate_mochi_id_lesson`
- **Assertions:**
	- Ensure that the correct deck structure is created in Mochi.
	- Verify that the Airtable records are updated with the correct Mochi deck IDs.

2. **`test_sync_cards`**
- **Description:** Tests the `sync_cards` method to ensure it correctly synchronizes the vocab cards between Airtable and Mochi.
- **Mocked Dependencies:**
	- `ConnectAirtableAPI.get_cards_to_create`
	- `MochiAPI.create_card_chinese`
	- `MochiAPI.create_card_english`
	- `ConnectAirtableAPI.populate_mochi_id_vocab`
- **Assertions:**
	- Ensure that the correct cards are created in Mochi.
	- Verify that the Airtable records are updated with the correct Mochi card IDs.

---
### `mochi_API_test.py`

**Purpose:**
This test file is responsible for testing the `MochiAPI` class methods. The tests ensure that the methods correctly interact with the Mochi API to perform operations like creating decks and cards.

**Unit Tests:**
1. **`test_create_deck`**
- **Description:** Tests the `create_deck` method to ensure it successfully creates a deck in Mochi and returns the deck ID.
- **Mocked Dependencies:**
	- Mochi API's `requests.post` method.
- **Assertions:**
	- Ensure the correct payload is sent to the Mochi API.
	- Verify that the returned deck ID matches the expected value.

2. **`test_create_card_chinese`**
- **Description:** Tests the `create_card_chinese` method to ensure it successfully creates a card with the Chinese-first template in Mochi.
- **Mocked Dependencies:**
	- Mochi API's `requests.post` method.
- **Assertions:**
	- Verify that the correct payload is sent to the Mochi API.
	- Ensure the correct card ID is returned.

3. **`test_create_card_english`**
- **Description:** Tests the `create_card_english` method to ensure it successfully creates a card with the English-first template in Mochi.
- **Mocked Dependencies:**
	- Mochi API's `requests.post` method.
- **Assertions:**
	- Verify that the correct payload is sent to the Mochi API.
	- Ensure the correct card ID is returned.

4. **`test_get_cards`**
- **Description:** Tests the `get_cards` method to ensure it retrieves all cards from Mochi for a given deck.
- **Mocked Dependencies:**
	- Mochi API's `requests.get` method.
- **Assertions:**
	- Verify that the correct API endpoint is called.
	- Ensure the correct list of cards is returned.

5. **`test_get_all_decks`**
- **Description:** Tests the `get_all_decks` method to ensure it retrieves all decks from Mochi.
- **Mocked Dependencies:**
	- Mochi API's `requests.get` method.
- **Assertions:**
	- Verify that the API call handles pagination correctly.
	- Ensure the correct list of decks is returned.

6. **`test_get_deck_id`**
- **Description:** Tests the `get_deck_id` method to ensure it correctly retrieves the deck ID for a given deck name.
- **Mocked Dependencies:**
	- `MochiAPI.get_all_decks` method.
- **Assertions:**
	- Ensure the correct deck ID is returned for a given name.
	- Verify that `None` is returned if the deck name is not found.


### `chinese_dict_lookup_test.py`

**Purpose:**
This test file ensure that the methods return correct pinyin, translations, and handle lists of vocabulary items appropriately.

**Unit Tests:**
1. **Test: `test_get_pinyin_translation`**
    - **Description:** Tests the `get_pinyin_translation` method to ensure it correctly returns the pinyin and translation for a given Chinese word.
    - **Mocked Dependencies:**
        - `CcCedict.get_entry` is mocked to return a predefined dictionary with the expected translation.
    - **Assertions:**
        - Checks if the pinyin is `xī shī quǎn`.
        - Checks if the translation is `shih tzu (dog breed)`.

1. **Test: `test_format_pinyin_from_char`**
    - **Description:** Tests the `format_pinyin_from_char` method to ensure it correctly formats the pinyin for a given Chinese character string.
    - **Assertions:**
        - Checks if the formatted pinyin is `xī shī quǎn`.

1. **Test: `test_lookup_vocab_list`**
    - **Description:** Tests the `lookup_vocab_list` method to ensure it correctly processes a list of vocabulary words, providing pinyin and translations for each.
    - **Assertions:**
        - Checks if the result matches the expected list of dictionaries, each containing the word, its pinyin, and its translation.
---

## Running the Tests

To run the tests, use the following command:

```bash
python -m unittest discover -s tests -p '*_test.py'
```

Or, if using `pytest`:

```bash
pytest
```

---

## Conclusion

These unit tests cover the core functionalities of the `ChineseVocabLookup`,  `ConnectAirtableAPI` , `AirtableMochiSync`, and  `MochiAPI` classes. By mocking external dependencies, the tests ensure that the synchronization logic between Airtable and Mochi operates as expected without making actual API calls. 

---