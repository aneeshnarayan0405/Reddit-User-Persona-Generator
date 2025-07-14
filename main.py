from scraper import RedditScraper
from persona_builder import PersonaBuilder
import argparse
import json
import os
from urllib.parse import urlparse

def extract_username(url):
    """Extract username from Reddit profile URL"""
    path = urlparse(url).path
    if path.startswith('/user/'):
        return path.split('/')[2]
    elif path.startswith('/u/'):
        return path.split('/')[2]
    return None

def save_persona(persona, filename):
    """Save persona to a text file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Reddit User Persona Analysis\n")
        f.write(f"="*40 + "\n\n")
        f.write(f"Username: {persona['username']}\n\n")
        
        f.write(f"Basic Statistics:\n")
        f.write(f"- Total comments: {persona['basic_stats']['total_comments']}\n")
        f.write(f"- Total submissions: {persona['basic_stats']['total_submissions']}\n")
        f.write("\n")
        
        f.write(f"Top Interests (based on subreddit activity):\n")
        for subreddit, count in persona['interests']:
            f.write(f"- {subreddit}: {count} interactions\n")
        f.write("\n")
        
        f.write(f"Sentiment Analysis (compound score ranges from -1 to 1):\n")
        f.write(f"- Positive: {persona['sentiment_analysis']['pos']:.2f}\n")
        f.write(f"- Negative: {persona['sentiment_analysis']['neg']:.2f}\n")
        f.write(f"- Neutral: {persona['sentiment_analysis']['neu']:.2f}\n")
        f.write(f"- Compound: {persona['sentiment_analysis']['compound']:.2f}\n")
        f.write("\n")
        
        f.write(f"Detailed Persona Analysis:\n")
        f.write("="*40 + "\n")
        f.write(persona['detailed_persona'])
        f.write("\n\n")
        
        f.write(f"Top Keywords:\n")
        for word, count in persona['keywords']:
            f.write(f"- {word} ({count} occurrences)\n")

def main():
    parser = argparse.ArgumentParser(description='Reddit User Persona Generator')
    parser.add_argument('url', type=str, help='Reddit user profile URL')
    parser.add_argument('--output', type=str, default=None, help='Output file path')
    
    args = parser.parse_args()
    
    username = extract_username(args.url)
    if not username:
        print("Error: Invalid Reddit profile URL")
        return
    
    print(f"Starting analysis for user: {username}")
    
    # Scrape data
    scraper = RedditScraper()
    data = scraper.get_user_data(username)
    
    # Build persona
    builder = PersonaBuilder()
    persona = builder.build_persona(data)
    
    # Save output
    output_file = args.output if args.output else f"{username}_persona.txt"
    save_persona(persona, output_file)
    
    print(f"Persona analysis saved to: {output_file}")

if __name__ == "__main__":
    main()
