import openai
import os
from dotenv import load_dotenv
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import defaultdict
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

nltk.download('vader_lexicon')

class PersonaBuilder:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, text):
        return self.sia.polarity_scores(text)
    
    def extract_keywords(self, texts):
        # Simple keyword extraction - can be enhanced
        word_counts = defaultdict(int)
        for text in texts:
            words = text.lower().split()
            for word in words:
                if len(word) > 4:  # Ignore short words
                    word_counts[word] += 1
        return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    def analyze_interests(self, data):
        subreddit_counts = defaultdict(int)
        for comment in data["comments"]:
            subreddit_counts[comment["subreddit"]] += 1
        for submission in data["submissions"]:
            subreddit_counts[submission["subreddit"]] += 1
        return sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def generate_persona_with_gpt(self, data):
        try:
            prompt = f"""Analyze this Reddit user's activity and create a detailed persona:
            
            Username: {data['username']}
            
            Activity Summary:
            - {len(data['comments'])} comments
            - {len(data['submissions'])} submissions
            - Top subreddits: {', '.join([s[0] for s in self.analyze_interests(data)])}
            
            Create a comprehensive user persona with these sections:
            1. Demographics (inferred)
            2. Interests (based on subreddit activity and content)
            3. Personality Traits (based on writing style and sentiment)
            4. Behavioral Patterns (posting frequency, engagement)
            5. Values/Beliefs (based on expressed opinions)
            
            For each characteristic, include 1-2 direct quotes from their posts/comments that support your analysis.
            Format the persona professionally with clear section headers.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a skilled analyst who creates detailed user personas from online activity."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating persona with GPT: {e}")
            return None
    
    def build_persona(self, data):
        persona = {
            "username": data["username"],
            "basic_stats": {
                "total_comments": len(data["comments"]),
                "total_submissions": len(data["submissions"]),
                "first_activity": min(
                    [c["created_utc"] for c in data["comments"]] + 
                    [s["created_utc"] for s in data["submissions"]]
                ) if data["comments"] or data["submissions"] else None,
                "last_activity": max(
                    [c["created_utc"] for c in data["comments"]] + 
                    [s["created_utc"] for s in data["submissions"]]
                ) if data["comments"] or data["submissions"] else None
            },
            "interests": self.analyze_interests(data),
            "sentiment_analysis": self.analyze_sentiment(
                " ".join([c["body"] for c in data["comments"]] + 
                        [s["title"] + " " + s["selftext"] for s in data["submissions"]])
            ),
            "keywords": self.extract_keywords(
                [c["body"] for c in data["comments"]] + 
                [s["title"] + " " + s["selftext"] for s in data["submissions"]]
            ),
            "detailed_persona": self.generate_persona_with_gpt(data)
        }
        
        return persona
