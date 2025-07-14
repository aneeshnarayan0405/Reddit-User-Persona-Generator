import praw
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
    
    def get_user_data(self, username):
        """Fetch user comments and submissions"""
        user = self.reddit.redditor(username)
        
        print(f"Fetching data for user: {username}")
        
        comments = []
        submissions = []
        
        # Get comments with progress bar
        try:
            for comment in tqdm(user.comments.new(limit=None), desc="Fetching comments"):
                comments.append({
                    "body": comment.body,
                    "subreddit": str(comment.subreddit),
                    "created_utc": comment.created_utc,
                    "score": comment.score,
                    "permalink": comment.permalink
                })
        except Exception as e:
            print(f"Error fetching comments: {e}")
        
        # Get submissions with progress bar
        try:
            for submission in tqdm(user.submissions.new(limit=None), desc="Fetching submissions"):
                submissions.append({
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "subreddit": str(submission.subreddit),
                    "created_utc": submission.created_utc,
                    "score": submission.score,
                    "permalink": submission.permalink
                })
        except Exception as e:
            print(f"Error fetching submissions: {e}")
        
        return {
            "username": username,
            "comments": comments,
            "submissions": submissions
        }
