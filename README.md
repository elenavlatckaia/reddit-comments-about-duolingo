# Reddit Duolingo Comments Analysis

This project collects comments from three Duolingo-related subreddits to analyze how people discuss language learning on Reddit.

## Technical Details

### Libraries Used

The program uses several Python libraries:
- `PRAW` (Python Reddit API Wrapper): Main library to interact with Reddit
- `pandas`: For handling and saving data in CSV format
- `python-dotenv`: For secure storage of Reddit API credentials
- `datetime`: For adding timestamps to our files
- `time`: For tracking how long the data collection takes

### Reddit API Access

To collect data from Reddit, we use their official API through PRAW. This requires:
1. A Reddit account
2. Reddit API credentials (obtained from https://www.reddit.com/prefs/apps/):
   - Client ID
   - Client Secret
   - User Agent (identifies our program to Reddit)

These credentials are stored securely in a `.env` file and loaded using python-dotenv.

### How the Code Works

1. **Setup and Configuration**:
   - The program defines which subreddits to collect from
   - Sets how many comments to gather per subreddit (2000)
   - Loads Reddit API credentials from the `.env` file

2. **Data Collection Process**:
   - Connects to Reddit using PRAW
   - For each subreddit:
     * Gets the 100 "hot" posts
     * For each post, collects all comments
     * Stores comment data in a structured format
     * Shows real-time progress

3. **Data Storage**:
   - Uses pandas to organize the data
   - Creates separate CSV files for each subreddit
   - Makes one combined CSV with all comments
   - Adds timestamps to filenames for tracking different collection runs

## Data Collection Process

### What the Program Does

The program automatically collects comments from three Duolingo-related communities on Reddit:
- r/duolingo (official Duolingo subreddit)
- r/duolingomemes (memes about Duolingo)
- r/shitduolingosays (funny or strange sentences from Duolingo)

### How It Works

1. **Connection to Reddit**: The program uses official Reddit credentials to connect to Reddit's API (like having a special key to access Reddit's data)

2. **Gathering Comments**: For each subreddit, the program:
   - Looks at the most popular ("hot") posts
   - Collects comments from these posts
   - Tries to gather 2000 comments from each subreddit
   - Shows progress in real-time (how many comments collected, time spent)

3. **Saving Data**: The program creates:
   - Individual CSV files for each subreddit
   - One combined CSV file with all comments

## About the Dataset

### What's in the Data (Columns)

Each comment in our dataset includes:
- `comment_id`: Unique identifier for each comment
- `comment_text`: The actual text of the comment
- `score`: Number of upvotes minus downvotes (shows how popular the comment is)
- `created_utc`: When the comment was posted
- `author`: Username of who wrote the comment
- `post_title`: Title of the post the comment was made on
- `subreddit`: Which of the three communities the comment is from

### Dataset Statistics

Total comments collected: 3,269

Breakdown by subreddit:
- r/duolingo: 2,000 comments
- r/duolingomemes: 834 comments
- r/shitduolingosays: 435 comments

### Why Different Numbers?

While we aimed for 2,000 comments from each subreddit, we got different amounts because:
1. Smaller subreddits have fewer posts and comments available
2. r/duolingomemes and r/shitduolingosays are smaller communities compared to the main r/duolingo subreddit
3. The program only looks at recent "hot" posts, so if a subreddit is less active, it will have fewer comments to collect