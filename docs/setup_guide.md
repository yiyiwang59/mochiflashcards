
# Setup Guide for Airtable-Mochi Sync

## Prerequisites

1. **Airtable Account**: If you don't already have an Airtable account, you can sign up [here](https://airtable.com/).
2. **Mochi Account**: If you don't have a Mochi account, sign up [here](https://mochi.cards/).
3. **Python Environment**: Make sure you have Python 3.8+ installed. You can download it [here](https://www.python.org/downloads/).

## Step 1: Setting Up the Airtable Base

### 1.1 Create a New Base

- Log in to your Airtable account.
- Click on "Add a base" to create a new base. You can name it something like `Chinese`.

### 1.2 Create Tables

#### 1.2.1 Lessons Table

- **Table Name**: `Lessons`
- **Fields**:
  - `Lesson Name` (Single line text)
  - `Type` (Single select: "Conversation Topics", "Songs", etc.)
  - `Mochi Deck ID` (Single line text)

#### 1.2.2 Vocabulary Table

- **Table Name**: `Vocabulary`
- **Fields**:
  - `Name` (Chinese) (Single line text)
  - `English` (Single line text)
  - `Pinyin` (Single line text)
  - `Deck Name` (Link to `Lessons` table)
  - `Mochi Card ID (Chinese First)` (Single line text)
  - `Mochi Card ID (English First)` (Single line text)

### 1.3 Retrieve Airtable API Key and Base ID

- Go to your Airtable account settings to find your API key. (Builder Hub > [Personal Tokens](https://airtable.com/create/tokens) > Create Personal Token and grant access to your `Chinese` Base
- Find your Base ID from the API documentation. (Help > API Documentation)

**Example**:
```plaintext
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_airtable_base_id
```

## Step 2: Setting Up Mochi Templates

### 2.1 Create Templates in Mochi

- Log in to your Mochi account.
- Navigate to the Templates section.

#### 2.1.1 Chinese First Template

- **Template Name**: `Chinese First`
- **Fields**:
  - `Chinese` (Text)
  - `English` (Text)
  - `Pinyin` (Text)

#### 2.1.2 English First Template

- **Template Name**: `English First`
- **Fields**:
  - `English` (Text)
  - `Chinese` (Text)
  - `Pinyin` (Text)

### 2.2 Retrieve Template IDs

- Go to each template and copy the template ID. (`...` > "Copy ID")
- For each field within the template, copy the field IDs. (Click on field in template > "Copy field ID")

**Example**:
```plaintext
MOCHI_TEMPLATE_CHINESE=your_chinese_template_id
MOCHI_TEMPLATE_ENGLISH=your_english_template_id
MOCHI_TEMPLATE_CHINESE_FIELD_ENG=your_english_field_id
MOCHI_TEMPLATE_CHINESE_FIELD_CH=your_chinese_field_id
MOCHI_TEMPLATE_CHINESE_FIELD_PY=your_pinyin_field_id
MOCHI_TEMPLATE_ENGLISH_FIELD_ENG=your_english_field_id
MOCHI_TEMPLATE_ENGLISH_FIELD_CH=your_chinese_field_id
MOCHI_TEMPLATE_ENGLISH_FIELD_PY=your_pinyin_field_id
```

## Step 3: Setting Up Your Python Environment

### 3.1 Clone the Repository

```bash
git clone https://github.com/yiyiwang59/mochiflashcards.git
cd mochiflashcards
```

### 3.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.3 Configure Environment Variables

- Create a `.env` file in the root directory of your project and add the following:

```plaintext
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_airtable_base_id
MOCHI_API_TOKEN=your_mochi_api_token
MOCHI_TEMPLATE_CHINESE=your_chinese_template_id
MOCHI_TEMPLATE_ENGLISH=your_english_template_id
MOCHI_TEMPLATE_CHINESE_FIELD_ENG=your_english_field_id
MOCHI_TEMPLATE_CHINESE_FIELD_CH=your_chinese_field_id
MOCHI_TEMPLATE_CHINESE_FIELD_PY=your_pinyin_field_id
MOCHI_TEMPLATE_ENGLISH_FIELD_ENG=your_english_field_id
MOCHI_TEMPLATE_ENGLISH_FIELD_CH=your_chinese_field_id
MOCHI_TEMPLATE_ENGLISH_FIELD_PY=your_pinyin_field_id
```

## Step 4: Running the Script

### 4.1 Sync Decks

```bash
python airtable_mochi_sync.py --sync-decks
```

### 4.2 Sync Cards

```bash
python airtable_mochi_sync.py --sync-cards
```
