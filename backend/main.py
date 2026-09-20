from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI(
    title="FlashFeed API",
    description="AI-powered personalized news platform",
    version="0.1.0"
)

# temp in-memory data for testing prototype
articles = [
    {
        "id": 1,
        "title": "Example AI News",
        "category": "AI",
        "source": "Demo Source",
        "summary": "This is a temporary article."
    },
    {
        "id": 2,
        "title": "Example Backend News",
        "category": "Backend",
        "source": "Demo Source",
        "summary": "This is another temporary article."
    }
]

# defining Pydantic models

class ArticleCreate(BaseModel):
    title: str
    category: str
    source: str
    summary: Optional[str] = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    category: str
    source: str
    summary: Optional[str] = None


# basic routes

@app.get("/")
def root():
    return {
        "message": "Welcome to FlashFeed"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

# article routes

@app.get("/articles", response_model=list[ArticleResponse])
def get_articles():
    return articles


@app.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int):

    for article in articles:
        if article["id"] == article_id:
            return article

    raise HTTPException(
        status_code=404,
        detail="Article not found"
    )


@app.post("/articles", response_model=ArticleResponse)
def create_article(article: ArticleCreate):

    new_article = {
        "id": len(articles) + 1,
        "title": article.title,
        "category": article.category,
        "source": article.source,
        "summary": article.summary
    }

    articles.append(new_article)

    return new_article


@app.delete("/articles/{article_id}")
def delete_article(article_id: int):

    for index, article in enumerate(articles):

        if article["id"] == article_id:

            articles.pop(index)

            return {
                "message": "Article deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Article not found"
    )


# category roots

@app.get("/categories")
def get_categories():

    categories = set(
        article["category"]
        for article in articles
    )

    return {
        "categories": list(categories)
    }

