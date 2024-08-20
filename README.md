
# Airtable Mochi Sync

Airtable Mochi Sync is a Python-based tool designed to synchronize data between Airtable and Mochi Cards. This project allows you to automatically create decks and cards in Mochi based on data stored in Airtable, ensuring that your flashcard collection is always up-to-date with your learning material.

## Features

- **Sync Airtable Lessons to Mochi:** The tool handles the creation of decks and cards in Mochi based on the information provided in Airtable.
- **Populate Vocabulary:** Populate english translation and pronunciation (pinyin) from just Chinese characters directly in Airtable
- **Mochi Deck and Card creation multiple templates:** The tool handles the creation of decks and cards in Mochi with both Chinese-first and English-first templates for a given vocab set

## Installation

### Prerequisites

- Python 3.8 or higher
- Pip (Python package installer)
- A Mochi premium account ($5/month) - required to use their API
- Airtable Account with a Chinese Base and 2 Tables (Vocab and Lessons)

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yiyiwang59/mochiflashcards.git
    cd mochiflashcards
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory with the following variables:
   ```
	AIRTABLE_API_TOKEN = airtable_token
	AIRTABLE_BASE_ID = airtable_chinese_base_id
	AIRTABLE_VOCAB_TABLE_ID = airtable_vocab_table_ID
	AIRTABLE_LESSON_TABLE_ID = airtable_lesson_table_ID
	AIRTABLE_ENGLISH_TRANSLATION_ID = airtable_english_translation_field_id
	AIRTABLE_CH_VOCAB_ID = airtable_vocab_field_id
	AIRTABLE_PINYIN_ID = airtable_pinyin_field_id
	AIRTABLE_LESSON_NAME_ID = airtable_lesson_name_field_id
	AIRTABLE_LESSON_TYPE_ID = airtable_lesson_type_field_id
	AIRTABLE_MOCHI_DECK_ID = airtable_mochi_deck_field_id
	AIRTABLE_MOCHI_CARD_CH_ID = airtable_mochi_card_chinese_template_field_id
	AIRTABLE_MOCHI_CARD_ENG_ID = airtable_mochi_card_english_template_field_id
	
	
	MOCHI_API_TOKEN = mochi_token
	MOCHI_TEMPLATE_CHINESE = mochi_template_chinese_ID
	MOCHI_TEMPLATE_CHINESE_FIELD_ENG = mochi_chinese_template_english_field_id
	MOCHI_TEMPLATE_CHINESE_FIELD_CH = mochi_chinese_template_chinese_field_id
	MOCHI_TEMPLATE_CHINESE_FIELD_PY = mochi_chinese_template_pinyin_field_id
	MOCHI_TEMPLATE_ENGLISH_ID = mochi_template_english_ID
	MOCHI_TEMPLATE_ENGLISH_FIELD_ENG = mochi_english_template_english_field_id
	MOCHI_TEMPLATE_ENGLISH_FIELD_CH = mochi_english_template_chinese_field_id
	MOCHI_TEMPLATE_ENGLISH_FIELD_PY = mochi_english_template_pinyin_field_id
	```

4. Run the script:
	```bash
	python main.py
	```

## Usage

The script provides three main functionalities:

1. **Chinese Dictionary Lookup**: Populates English translation and pronunciation (pinyin) columns in Airtable for the Chinese Vocabulary you populate in the Vocab column
2. **Sync Decks**: Creates decks in Mochi based on lessons in Airtable.
3. **Sync Cards**: Creates vocabulary cards in Mochi based on data in Airtable.

## Testing

Unit tests are provided to ensure the correct functionality of the sync operations.

Run the tests using:
```bash
python -m unittest discover -s tests -p '*_test.py'
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to follow the code style guidelines and add appropriate tests for any new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact yiyiwang5959@gmail.com.
