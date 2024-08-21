### Project Overview

**Project Name:** Mochiflashcards (Current State), Chinese Vocab Study Material (Future State)
**Objective:** To create a seamless integration between Airtable and Mochi Cards, allowing the automated creation of decks and cards in Mochi based on data stored in Airtable.

### Table of Contents

1. [Introduction](#introduction)
2. [Data Flow](#data-flow)
   - [Deck Creation](#deck-creation)
   - [Card Creation](#card-creation)
3. [Class and Module Descriptions](#class-and-module-descriptions)
   - [ConnectAirtableAPI Class](#connectairtableapi-class)
   - [MochiAPI Class](#mochiapi-class)
   - [AirtableMochiSync Class](#airtablemochisync-class)
4. [API Integration Details](#api-integration-details)
   - [Airtable API](#airtable-api)
   - [Mochi API](#mochi-api)
5. [Error Handling](#error-handling)
6. [Future Enhancements](#future-enhancements)

---

### Introduction

This project integrates Airtable and Mochi Cards to automate the process of creating study decks and flashcards based on a structured data set in Airtable. The goal is to minimize manual data entry and ensure consistency between the two platforms.

---

### Data Flow

#### Deck Creation

1. **Airtable Lessons Table:**
   - **Input:** Contains lessons with fields for `Lesson Name`, `Lesson Type`, and `Mochi Deck ID`.
   - **Process:** 
     - The system retrieves lessons from Airtable that do not have corresponding Mochi Deck IDs.
     - Each lesson's `Lesson Type` is checked to determine if a parent deck exists in Mochi. If not, a parent deck is created.
     - A Mochi deck is created for each lesson under the relevant parent deck (if applicable).
     - The Mochi Deck ID is then stored back in Airtable in the `Mochi Deck ID` field.

2. **Deck Hierarchy:**
   - **Parent Deck:** Represents categories like "Conversation Topics" or "Songs."
   - **Child Deck:** Represents individual lessons like "Pets" or "Career."

#### Card Creation

1. **Airtable Vocab Table:**
   - **Input:** Contains vocab words associated with lessons, with fields for `Vocab (Name)`, `English`, `Pinyin`, `Lesson ID`, `Mochi Card ID (Chinese)`, and `Mochi Card ID (English)`.
   - **Process:**
     - The system retrieves vocab words that do not have corresponding Mochi Card IDs.
     - Each vocab word is assigned to the relevant Mochi deck based on its associated `Lesson ID`.
     - Two cards are created for each vocab word: one with Chinese first and another with English first.
     - The Mochi Card IDs are then stored back in Airtable fields `Mochi Card ID (Chinese)`, and `Mochi Card ID (English)`.

---

### Class and Module Descriptions
#### ChineseVocabLookup Class

- **Purpose:** Handles the lookup and reformatting of pinyin and english translation based on Chinese vocab.
- **Key Methods:**
  - `get_pinyin_translation(word)`: Retrieves the pinyin and english translation by looking up the chinese word
  - `format_pinyin_from_char(char_input)`: Reformats pinyin from tone numbers (ni2 hao3) to tone symbols (ní hǎo)
  - `lookup_vocab_list(vocab_list)`: Loops through an array of chinese vocab and applies the `get_pinyin_translation()` to each item, returning an array of the chinese vocab word, pinyin, and translation for each word in the `vocab_list`

#### ConnectAirtableAPI Class

- **Purpose:** Handles all interactions with the Airtable API.
- **Key Methods:**
  - `get_missing_translation_records()`:  Retrieves the vocab words from the `Chinese Vocab` Table where the `English` field is blank
  - `fill_in_missing_data()`: Uses the `ChineseVocabLookup` class to lookup the pinyin and english translation and populate the `Pinyin` and `English` columns in Airtable
  - `get_decks_to_create()`: Retrieves lessons from Airtable that need corresponding Mochi decks.
  - `get_cards_to_create()`: Retrieves vocab words from Airtable that need corresponding Mochi cards.
  - `populate_mochi_id_lesson(at_id, mochi_deck_id)`: Updates Airtable with the Mochi Deck ID for a lesson.
  - `populate_mochi_id_vocab(at_vocab_id, mochi_card_id_ch, mochi_card_id_eng)`: Updates Airtable with the Mochi Card IDs for a vocab word.

#### MochiAPI Class

- **Purpose:** Manages all interactions with the Mochi API.
- **Key Methods:**
  - `create_deck(name, parent_deck_id)`: Creates a new deck in Mochi and assigns it in the proper parent deck hierarchy.
  - `create_card_chinese(chinese, english, pinyin, deck)`: Creates a new card with Chinese first template.
  - `create_card_english(chinese, english, pinyin, deck)`: Creates a new card with English first template.
  - `get_cards(deck_id=None)`: Retrieves all mochi cards with the `mochi_id`, `chinese`, `english`, `pinyin`, `mochi_deck_id`
  - `get_all_decks()`: Retrieves all Mochi decks with the `Deck Name` and `Mochi Deck ID`
  - `get_deck_id(deck_name)`: Retrieves a Mochi Deck ID based on the deck name by calling the `get_all_decks()` function and finding a match with the deck name.

#### AirtableMochiSync Class

- **Purpose:** Acts as the main manager that coordinates the syncing process between Airtable and Mochi.
- **Key Methods:**
  - `sync_decks()`: Syncs lessons from Airtable with decks in Mochi.
  - `sync_cards()`: Syncs vocab words from Airtable with cards in Mochi.

---

### API Integration Details

#### Airtable API

- **Base URL:** `https://api.airtable.com/v0/{base_id}/`
- **Authentication:** Uses a Bearer token stored in environment variables.
- **Rate Limits:** Be mindful of the rate limits imposed by Airtable, typically 5 requests per second.
- **Endpoints:**
  - `get_decks_to_create()`: Queries Airtable for lessons that need decks created in Mochi.
  - `get_cards_to_create()`: Queries Airtable for vocab words that need cards created in Mochi.
  - `populate_mochi_id_lesson(at_id, mochi_deck_id)`: Populates Airtable column in `Chinese Lessons` table with Mochi Deck ID
  - `populate_mochi_id_vocab(at_vocab_id, mochi_card_id_ch, mochi_card_id_eng)`: Populates Airtable columns in `Chinese vocab` table with Mochi Card IDs

#### Mochi API

- **Base URL:** `https://app.mochi.cards/api/`
- **Authentication:** Uses HTTP Basic Authentication with the API token as the username.
- **Endpoints:**
  - `create_deck`: Creates a new deck in Mochi.
  - `create_card`: Creates a new card in Mochi.
  - `get_decks`: Retrieves all decks from Mochi.
  
---

### Error Handling (Future State)

- **Network Errors:** Implement retries with exponential backoff for handling temporary network issues.
- **API Rate Limits:** Monitor rate limits and include handling to pause and resume requests when limits are reached.
- **Missing Data:** Ensure that required fields (like `Lesson Type`) are present in Airtable before attempting to create decks or cards.

---

### Future Enhancements

- **Enhanced Logging:** Implement detailed logging for better traceability of errors and processing steps.
- **Conflict Resolution:** Develop a system to handle potential conflicts when decks or cards already exist in Mochi.
- **Error Handling**: Develop a proper error-handling system for any potential edge cases
- **Bi-di Sync**: Currently can only create net new decks, will add ability to make changes to existing decks from either airtable or mochi and have it sync bi-directionally
- **Generate Writing Practice PDF**: Generate a PDF of all the vocab words in a set in a traditional chinese character writing practice worksheet
- **Generate Vocab Quiz PDF**: Generate PDF of a handwritten vocab quiz for the vocab set
- **Add csv integration**: Ability to generate writing practice PDF, Vocab Quiz PDF, and Mochi Flashcards through just a csv of vocab words submitted

---

This detailed design document provides a comprehensive overview of the Chinese Vocab Study Material project, covering the core functionalities, data flow, and class/module responsibilities. It also includes details on how the Airtable and Mochi APIs are integrated and outlines areas for future enhancement.