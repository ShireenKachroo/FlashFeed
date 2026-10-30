from apscheduler.schedulers.background import BackgroundScheduler
from .ingest import fetch_and_store_news

def start_scheduler():
    scheduler = BackgroundScheduler()

    # fetches news every 6hrs
    scheduler.add_job(fetch_and_store_news, 'interval', hours=6)

    scheduler.start()
    print("Background RSS Ingestion Scheduler started...")