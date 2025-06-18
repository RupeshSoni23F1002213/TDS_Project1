import json
import sqlite3
import os
from datetime import datetime

DB_PATH = "knowledge_base.db"
JSON_PATH = "discourse_posts.json"

def insert_discourse_chunks():
    if not os.path.exists(JSON_PATH):
        print(f"{JSON_PATH} not found.")
        return

    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        posts = json.load(file)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for idx, post in enumerate(posts):
        content = post.get('content', '')
        # Use defaults for missing fields
        post_id = post.get('post_id', None)
        topic_id = post.get('topic_id', None)
        topic_title = post.get('topic_title', None)
        post_number = post.get('post_number', idx + 1)
        author = post.get('author', 'unknown')
        created_at = post.get('created_at', datetime.now().isoformat())
        likes = post.get('likes', 0)
        chunk_index = post.get('chunk_index', 0)
        url = post.get('url', '')
        embedding = post.get('embedding', None)

        c.execute('''
            INSERT INTO discourse_chunks (
                post_id, topic_id, topic_title, post_number, author, created_at, likes, chunk_index, content, url, embedding
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post_id,
            topic_id,
            topic_title,
            post_number,
            author,
            created_at,
            likes,
            chunk_index,
            content,
            url,
            embedding
        ))

    conn.commit()
    conn.close()
    print(f"Inserted {len(posts)} posts into discourse_chunks.")

if __name__ == "__main__":
    insert_discourse_chunks()