from celery import Celery
from crawler import get_enterprises, save_as_json

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def crawl_enterprises():
    enterprises = get_enterprises()
    save_as_json(enterprises, 'enterprises.json')
    return f"Scraping completed. Data saved to enterprises.json"