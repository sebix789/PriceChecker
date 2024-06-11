from .celery import app
from .services import show_all, run_spider

@app.task
def run_spider_task_with_combined_keywords():
    try:
        products = show_all()
        for product in products:
            keywords = product['keywords']
            product_name = ' '.join(keywords)
            run_spider(product_name)
    except Exception as e:
        print(f"An error occurred: {e}")