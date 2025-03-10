# Anki Card Generator

This Python tool generates language learning flashcards for Anki using DeepSeek's AI. It creates contextually rich language expressions with translations, example sentences, and pronunciation resources.

## Features

- Generate customized language expressions based on target language and topic
- Specify CEFR proficiency level (A1-C2)
- Include contextual information, usage examples, and cultural notes
- Link to Forvo.com for audio pronunciations
- Export directly to Anki-compatible CSV format

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/anki-card-generator.git
cd anki-card-generator

# Install dependencies
pip install openai
```

## Usage

```bash
python anki_card_generator.py --target-language "Spanish" --topic "business expressions" --number 15 --cefr-level "B2" --api-key "your-deepseek-api-key"
```

### Required Arguments

- `--target-language`: Language for which to generate expressions (e.g., "Spanish")

### Optional Arguments

- `--native-language`: Your native language for translations (default: English)
- `--number`: Number of cards to generate (default: 10)
- `--topic`: Specific topic for the expressions (default: general)
- `--output`: Output CSV filename (default: anki_cards.csv)
- `--api-key`: DeepSeek API key (can also be set as DEEPSEEK_API_KEY environment variable)
- `--cefr-level`: CEFR proficiency level (A1, A2, B1, B2, C1, C2; default: B1)

## Output Format

The script generates a CSV file compatible with Anki import, containing fields like:
- Expression in target language
- Context of use
- Translation/meaning
- Literal translation (for idioms)
- Example sentence
- Example translation
- Cultural/usage notes
- CEFR level
- Audio URL link

## Example

```bash
python anki_card_generator.py --target-language "Spanish" --topic "business" --cefr-level "B1" --api-key "your-api-key"
```

This will create business-related Spanish expressions at B1 level, saving them to anki_cards.csv.

## License

MIT License