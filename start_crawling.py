from crawler_tasks import crawl_all_enterprises

result = crawl_all_enterprises.delay()
print("Crawling initiated. Please check the progress in the logs.")