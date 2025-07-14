# Reddit-User-Persona-Generator

# Reddit User Persona Generator 🔍

A sophisticated tool that analyzes Reddit users' activity to generate comprehensive personas using NLP and LLMs.

## Features ✨

- **Reddit API Integration**: Fetches complete comment and post history
- **Advanced NLP Analysis**: Sentiment, keyword extraction, and topic modeling
- **LLM-Powered Insights**: GPT-4 generates detailed persona narratives
- **Citation System**: Every trait is backed by actual user content
- **Professional Output**: Well-formatted text reports

## Tech Stack 🛠️

- Python 3.9+
- PRAW (Reddit API)
- OpenAI GPT-4
- NLTK for NLP
- tqdm for progress tracking
- python-dotenv for configuration

## Setup ⚙️

```bash
# Clone repository
git clone https://github.com/yourusername/reddit-user-persona.git
cd reddit-user-persona

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
