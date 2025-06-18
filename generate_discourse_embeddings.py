import os
import sqlite3
import requests
from dotenv import load_dotenv
import time
import json

DB_PATH = "knowledge_base.db"

# Load .env
load_dotenv()
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")  
API_KEY = os.getenv("API_KEY")  # If your API needs a key

def get_embedding(text):
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    data = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    response = requests.post(EMBEDDING_API_URL, headers=headers, json=data)
    if response.status_code != 200:
        print("Request body:", data)
        print("Response:", response.status_code, response.text)
        response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT id, content FROM discourse_chunks WHERE embedding IS NULL")
    rows = c.fetchall()
    print(f"Found {len(rows)} rows without embeddings.")

    for idx, (row_id, content) in enumerate(rows, 1):
        try:
            if not content or not content.strip():
                print(f"Skipping empty content for row {row_id}")
                continue
            embedding = get_embedding(content)
            # Store as JSON string (or adapt if you want to store as BLOB)
            c.execute("UPDATE discourse_chunks SET embedding = ? WHERE id = ?", (json.dumps(embedding), row_id))
            if idx % 10 == 0:
                conn.commit()
                print(f"Processed {idx}/{len(rows)} rows...")
            time.sleep(0.2)  # Adjust as needed for your API
        except Exception as e:
            print(f"Error processing row {row_id}: {e}")

    conn.commit()
    conn.close()
    print("Embedding generation complete.")

if __name__ == "__main__":
    main()