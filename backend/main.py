from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

# Import database session dependency and models
from backend.database import get_db
from backend.models import ArticleModel

# Import for CronJob
from .scheduler import start_scheduler

app = FastAPI(
    title="FlashFeed API",
    description="AI-powered personalized tech news platform",
    version="0.1.0"
)

@app.on_event("startup")
def startup_event():
    # as soon as fastapi starts, background scheduler will start
    start_scheduler()

# Pydantic Schemas for Request/Response validation
class ArticleCreate(BaseModel):
    title: str
    url: str
    source_name: str
    category: str
    summary: Optional[str] = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    source_name: str
    category: str
    summary: Optional[str] = None

    class Config:
        from_attributes = True  # Allows SQLAlchemy models to be read directly as Pydantic models


# Basic Routes
@app.get("/")
def root():
    return {"message": "Welcome to FlashFeed API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Database-Backed Article Routes

@app.get("/articles", response_model=list[ArticleResponse])
def get_articles(db: Session = Depends(get_db)):
    """Fetch all tech news articles from PostgreSQL."""
    articles = db.query(ArticleModel).all()
    return articles


@app.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Fetch a single article by its primary key ID."""
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.post("/articles", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    """Manually add an article to the database."""
    # Check if URL already exists to avoid duplicates
    existing_article = db.query(ArticleModel).filter(ArticleModel.url == article.url).first()
    if existing_article:
        raise HTTPException(status_code=400, detail="Article with this URL already exists")

    new_article = ArticleModel(
        title=article.title,
        url=article.url,
        source_name=article.source_name,
        category=article.category,
        summary=article.summary
    )
    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)  # Refresh to get the auto-generated ID and timestamp
    
    return new_article


@app.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    """Delete an article from the database."""
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully"}


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all unique categories currently present in the database."""
    categories = db.query(ArticleModel.category).distinct().all()
    # Flatten the list of tuples returned by SQLAlchemy distinct query
    category_list = [cat[0] for cat in categories]
    return {"categories": category_list}