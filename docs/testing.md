
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

## Unit Tests

### Test: `test_sync_decks`

**Tested Method:**
- `AirtableMochiSync.sync_decks()`

**Mocks:**
- `ConnectAirtableAPI.get_decks_to_create()`
- `MochiAPI.get_deck_id()`
- `MochiAPI.create_deck()`
- `ConnectAirtableAPI.populate_mochi_id_lesson()`

**Purpose:**
This test checks that the `sync_decks` method correctly handles the synchronization of decks between Airtable and Mochi. Specifically, it verifies:
- The correct decks are retrieved from Airtable.
- Deck IDs are fetched or created in Mochi based on the deck name.
- The correct mappings are populated in Airtable.

**Expected Behavior:**
- The method should create new decks in Mochi if they do not exist.
- The `populate_mochi_id_lesson` method should be called the correct number of times with the appropriate arguments.

**Assertions:**
- The test checks that the returned result matches the expected decks from Airtable.
- It verifies that the `populate_mochi_id_lesson` method was called with the correct arguments.

### Test: `test_sync_cards`

**Tested Method:**
- `AirtableMochiSync.sync_cards()`

**Mocks:**
- `ConnectAirtableAPI.get_cards_to_create()`
- `MochiAPI.get_deck_id()`
- `MochiAPI.create_card_chinese()`
- `MochiAPI.create_card_english()`
- `ConnectAirtableAPI.populate_mochi_id_vocab()`

**Purpose:**
This test checks that the `sync_cards` method correctly handles the synchronization of vocabulary cards between Airtable and Mochi. It verifies:
- Cards are correctly retrieved from Airtable.
- Corresponding cards are created in Mochi using both Chinese-first and English-first templates.
- The correct card IDs are populated back into Airtable.

**Expected Behavior:**
- The method should correctly create vocabulary cards in the specified deck.
- The `populate_mochi_id_vocab` method should be called with the correct arguments to update Airtable with the newly created Mochi card IDs.

**Assertions:**
- The test checks that the `populate_mochi_id_vocab` method was called the correct number of times with the expected arguments.

### Test: `test_create_deck`

**Tested Method:**
- `MochiAPI.create_deck()`

**Mocks:**
- `requests.post`

**Purpose:**
This test verifies that the `create_deck` method in the `MochiAPI` class correctly sends a POST request to the Mochi API to create a new deck.

**Expected Behavior:**
- The method should send a POST request to the correct URL with the correct payload and headers.
- The deck ID returned by the API should be correctly parsed and returned by the method.

**Assertions:**
- The test verifies that `requests.post` was called with the expected parameters.
- It checks that the returned deck ID matches the expected value from the mocked API response.

### Test: `test_create_card_chinese`

**Tested Method:**
- `MochiAPI.create_card_chinese()`

**Mocks:**
- `requests.post`

**Purpose:**
This test ensures that the `create_card_chinese` method correctly sends a POST request to create a Chinese-first card in the specified Mochi deck.

**Expected Behavior:**
- The method should correctly construct the payload with the Chinese, English, and Pinyin fields.
- The API call should return the correct card ID.

**Assertions:**
- The test checks that `requests.post` was called with the correct parameters and payload.
- It verifies that the returned card ID matches the expected value.

### Test: `test_create_card_english`

**Tested Method:**
- `MochiAPI.create_card_english()`

**Mocks:**
- `requests.post`

**Purpose:**
This test ensures that the `create_card_english` method correctly sends a POST request to create an English-first card in the specified Mochi deck.

**Expected Behavior:**
- The method should correctly construct the payload with the English, Chinese, and Pinyin fields.
- The API call should return the correct card ID.

**Assertions:**
- The test checks that `requests.post` was called with the correct parameters and payload.
- It verifies that the returned card ID matches the expected value.

### Test: `test_get_all_decks`

**Tested Method:**
- `MochiAPI.get_all_decks()`

**Mocks:**
- `requests.get`

**Purpose:**
This test ensures that the `get_all_decks` method correctly handles the pagination of results when retrieving all decks from the Mochi API.

**Expected Behavior:**
- The method should correctly handle multiple pages of results, using the bookmark for pagination.
- It should return a list of all decks with their corresponding IDs.

**Assertions:**
- The test checks that `requests.get` was called the expected number of times.
- It verifies that the returned list of decks matches the expected value based on the mocked API responses.

---

## Running the Tests

To run the tests, use the following command:

```bash
python -m unittest discover
```

Or, if using `pytest`:

```bash
pytest
```

---

## Conclusion

These unit tests cover the core functionalities of the `AirtableMochiSync` and `MochiAPI` classes. By mocking external dependencies, the tests ensure that the synchronization logic between Airtable and Mochi operates as expected without making actual API calls. 

---