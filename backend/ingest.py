#fetch articles from RSS feed, check duplicate URLs, save to DB

import feedparser
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import ArticleModel

# Selected Tech RSS Feeds
RSS_FEEDS = {
    "Hacker News": "https://news.ycombinator.com/rss",
    "Dev.to": "https://dev.to/feed",
    "TechCrunch": "https://techcrunch.com/feed/",
    "GitHub Blog": "https://github.blog/feed/"
}

def fetch_and_store_news():
    db: Session = SessionLocal()
    print("Starting news ingestion...")

    total_added = 0

    try:
        for source_name, feed_url in RSS_FEEDS.items():
            print(f"Fetching from {source_name}...")
            feed = feedparser.parse(feed_url)

            for entry in feed.entries:
                title = entry.get("title", "No Title")
                url = entry.get("link", "")

                # Basic validation: Skip if url or title is missing
                if not url or not title:
                    continue

                # Check if article already exists in database
                existing_article = db.query(ArticleModel).filter(ArticleModel.url == url).first()

                if not existing_article:
                    # Create new article record
                    new_article = ArticleModel(
                        title=title,
                        url=url,
                        source_name=source_name,
                        category="General Tech",  # Default category for now
                        summary=entry.get("summary", "No summary available")[:300] # Truncate if too long
                    )
                    db.add(new_article)
                    total_added += 1

        # Commit all new articles to the database
        db.commit()
        print(f"Ingestion complete! Successfully added {total_added} new articles.")

    except Exception as e:
        db.rollback()
        print(f"Error during ingestion: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fetch_and_store_news()