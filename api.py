import requests
import time
from typing import Set, Dict, Optional
from agents import get_agent

def get_new_posts():
    session = requests.Session()
    session.headers.update({'User-Agent': get_agent()})
    session.headers.update({'Accept': 'application/json'})
    
    resp = session.get(f"https://www.reddit.com/r/all/new/.json")
    print(resp.status_code)
    
    resp_json = resp.json()
    children = resp_json['data']['children']
    
    posts = []
    if children:
        for post in children:
            data = post['data']
            posts.append({
                "title": data['title'],
                "subreddit": data['subreddit'],
                "content": data['selftext'],
                "created_at": data['created'],
                "url": data['url'],
                "id": data['id'],
            })
    return posts

def get_new_comments():
    session = requests.Session()
    session.headers.update({'User-Agent': get_agent()})
    session.headers.update({'Accept': 'application/json'})
    
    resp = session.get(f"https://old.reddit.com/r/all/comments/.json")
    print(resp.status_code)
    
    resp_json = resp.json()
    children = resp_json['data']['children']
    
    comments = []
    if children:
        for comment in children:
            data = comment['data']
            comments.append({
                "parent_title": data['link_title'],
                "parent_id": data['parent_id'],
                "subreddit": data['subreddit'],
                "content": data['body'],
                "created_at": data['created'],
                "url": 'https://www.reddit.com' + data['permalink'],
                "id": data['id'],
            })
    return comments

def stream_new_posts(subreddits: str, interval: int = 600):
    seen_ids: Set[str] = set()
    
    while True:
        try:
            posts = get_new_posts(subreddits)
            for post in posts:
                if post['id'] not in seen_ids:
                    seen_ids.add(post['id'])
                    yield post
        except Exception as e:
            print(f"Error fetching posts: {e}")
        
        time.sleep(interval)

def stream_new_comments(subreddits: str, interval: int = 600):
    seen_ids: Set[str] = set()
    
    while True:
        try:
            comments = get_new_comments(subreddits)
            for comment in comments:
                if comment['id'] not in seen_ids:
                    seen_ids.add(comment['id'])
                    yield comment
        except Exception as e:
            print(f"Error fetching comments: {e}")
        
        time.sleep(interval)


if __name__ == "__main__":
    for post in stream_new_posts('memes+meme', interval=60):
        print(f"New post in r/{post['subreddit']}: {post['title']}")
