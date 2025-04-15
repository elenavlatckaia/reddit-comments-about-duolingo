import praw
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configuration
SUBREDDITS = [
    "duolingo",
    "duolingomemes",
    "shitduolingosays"
]
COMMENTS_PER_SUBREDDIT = 200000

def initialize_reddit():
    """Initialize Reddit API connection"""
    return praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )

def handle_rate_limit(e):
    """Handle rate limit errors by waiting the recommended time"""
    if hasattr(e.response, 'headers') and 'Retry-After' in e.response.headers:
        retry_after = int(e.response.headers['Retry-After'])
    else:
        retry_after = 60  # Default to 60 seconds if no header
    print(f"\nRate limit reached. Waiting {retry_after} seconds...")
    time.sleep(retry_after)

def gather_comments(subreddit_name, num_comments):
    """
    Gather comments from specified subreddit with rate limit handling
    """
    start_time = time.time()
    reddit = initialize_reddit()
    subreddit = reddit.subreddit(subreddit_name)
    comments_data = []
    
    try:
        print(f"\nGathering comments from r/{subreddit_name}...")
        submissions_count = 0
        for submission in subreddit.hot(limit=100000):
            submissions_count += 1
            try:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    if len(comments_data) >= num_comments:
                        break
                        
                    comments_data.append({
                        'comment_id': comment.id,
                        'comment_text': comment.body,
                        'score': comment.score,
                        'created_utc': datetime.fromtimestamp(comment.created_utc),
                        'author': str(comment.author),
                        'post_title': submission.title,
                        'subreddit': subreddit_name
                    })
                    
                    # Show progress every 100 comments
                    if len(comments_data) % 100 == 0:
                        elapsed_time = time.time() - start_time
                        comments_left = num_comments - len(comments_data)
                        print(f"\rProgress: {len(comments_data)}/{num_comments} comments | "
                              f"Elapsed time: {elapsed_time:.1f}s | "
                              f"Comments left: {comments_left} | "
                              f"Submissions: {submissions_count}", end='')
                
                if len(comments_data) >= num_comments:
                    break
                    
                # Add small delay between submissions to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                if hasattr(e, 'response') and e.response.status_code == 429:
                    handle_rate_limit(e)
                    continue
                else:
                    print(f"\nError processing submission: {str(e)}")
                    continue
            
        # Final progress update
        elapsed_time = time.time() - start_time
        print(f"\rCompleted: {len(comments_data)} comments gathered from {submissions_count} submissions in {elapsed_time:.1f} seconds")
                
    except Exception as e:
        print(f"\nAn error occurred with r/{subreddit_name}: {str(e)}")
        
    return comments_data

def save_to_csv(df, filename):
    """Helper function to save DataFrame to CSV"""
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    total_start_time = time.time()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    root_dir = f"./dataset_{timestamp}"
    os.makedirs(root_dir, exist_ok=False)

    all_comments = []
    
    print(f"Starting to gather comments from {len(SUBREDDITS)} subreddits...")
    
    # Gather comments from each subreddit
    for i, subreddit in enumerate(SUBREDDITS, 1):
        print(f"\nProcessing subreddit {i}/{len(SUBREDDITS)}: r/{subreddit}")
        comments = gather_comments(subreddit, COMMENTS_PER_SUBREDDIT)
        
        # Save individual subreddit data
        df = pd.DataFrame(comments)
        filename = f"{subreddit}_comments_{len(comments)}.csv"
        save_to_csv(df, os.path.join(root_dir, filename))
        
        all_comments.extend(comments)
    
    # Save combined data
    combined_df = pd.DataFrame(all_comments)
    combined_filename = f"combined_duo_comments_{len(all_comments)}.csv"
    save_to_csv(combined_df, os.path.join(root_dir, combined_filename))
    
    # Final statistics
    total_time = time.time() - total_start_time
    print(f"\nFinal Summary:")
    print(f"Total time elapsed: {total_time:.1f} seconds")
    print(f"Total comments gathered: {len(all_comments)}")
    print(f"Comments per subreddit:")
    for subreddit in SUBREDDITS:
        count = len([c for c in all_comments if c['subreddit'] == subreddit])
        print(f"r/{subreddit}: {count}")

if __name__ == "__main__":
    main() 