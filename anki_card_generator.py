import os
import json
import csv
import time
import argparse
from openai import OpenAI
from typing import List, Dict, Any

def setup_argparse() -> argparse.Namespace:
    """Set up command line arguments."""
    parser = argparse.ArgumentParser(description='Generate Anki cards for language learning using DeepSeek API')
    parser.add_argument('--target-language', type=str, required=True, help='Target language for the cards')
    parser.add_argument('--native-language', type=str, default='English', help='Your native language (default: English)')
    parser.add_argument('--number', type=int, default=10, help='Number of cards to generate (default: 10)')
    parser.add_argument('--topic', type=str, default='general', help='Topic for the expressions (default: general)')
    parser.add_argument('--output', type=str, default='anki_cards.csv', help='Output CSV filename (default: anki_cards.csv)')
    parser.add_argument('--api-key', type=str, help='DeepSeek API key (or set DEEPSEEK_API_KEY environment variable)')
    parser.add_argument('--cefr-level', type=str, default='B1', 
                        choices=['A1', 'A2', 'B1', 'B2', 'C1', 'C2'],
                        help='CEFR proficiency level (default: B1)')
    return parser.parse_args()

def generate_cards(api_key: str, target_language: str, native_language: str, num_cards: int, 
                   topic: str, cefr_level: str) -> List[Dict[str, str]]:
    """Generate language expression cards using DeepSeek API."""
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    system_prompt = """
    You are an expert linguist and language teacher specializing in creating high-quality language learning materials.
    You have deep knowledge of the Common European Framework of Reference for Languages (CEFR) levels and can accurately
    create language content appropriate for each level.
    """
    
    user_prompt = f"""
    Create {num_cards} useful, everyday expressions in {target_language} related to {topic} at CEFR level {cefr_level}.
    
    Format your response as a valid JSON array where each object has these fields:
    - expression: The expression in {target_language}
    - context: When/where this expression is typically used
    - meaning: Translation or meaning in {native_language}
    - literal: Word-for-word translation if it's an idiom (optional)
    - usage: An example sentence using this expression
    - translation: Translation of the example sentence in {native_language}
    - notes: Any cultural context, formality level, or grammar notes
    - cefr_level: The CEFR level of this expression (should match requested level: {cefr_level})
    - audio_url: A Forvo.com URL for pronunciation, if available (optional)
    
    Make sure the expressions are:
    - Appropriate for CEFR level {cefr_level} learners of {target_language}
    - Commonly used by native speakers
    - Useful for everyday conversation
    - Varied in formality levels
    - Include some idioms and colloquial phrases if appropriate for the level
    
    Return ONLY the JSON array with no additional text or explanation.
    """
    
    print(f"Generating {num_cards} {target_language} expressions at CEFR level {cefr_level} about {topic} with translations in {native_language}...")
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=4000
        )
        
        # Extract JSON from the response
        response_text = response.choices[0].message.content
        
        # Find JSON in the response (in case there's any extra text)
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
        else:
            raise ValueError("Could not find valid JSON array in response")
            
    except Exception as e:
        print(f"Error generating cards: {e}")
        return []

def save_to_csv(cards: List[Dict[str, str]], filename: str) -> None:
    """Save the generated cards to a CSV file for Anki import."""
    if not cards:
        print("No cards to save")
        return
    
    fieldnames = ['expression', 'context', 'meaning', 'literal', 'usage', 
                  'translation', 'notes', 'cefr_level', 'audio_url']
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Header row removed as requested
            writer.writerows(cards)
        
        print(f"Successfully saved {len(cards)} cards to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    args = setup_argparse()
    
    # Get API key from args or environment variable
    api_key = args.api_key or os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        print("Error: API key is required. Please provide it via --api-key or set the DEEPSEEK_API_KEY environment variable.")
        return
    
    # Generate cards
    cards = generate_cards(
        api_key=api_key,
        target_language=args.target_language,
        native_language=args.native_language,
        num_cards=args.number,
        topic=args.topic,
        cefr_level=args.cefr_level
    )
    
    # Save to CSV
    if cards:
        save_to_csv(cards, args.output)
        print(f"Example card: {json.dumps(cards[0], indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    main()