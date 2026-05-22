import praw

reddit = praw.Reddit(
    client_id="YOUR_ID",
    client_secret="YOUR_SECRET",
    user_agent="PulseSphere"
)

subreddit = reddit.subreddit("india")

for post in subreddit.hot(limit=10):
    print(post.title)