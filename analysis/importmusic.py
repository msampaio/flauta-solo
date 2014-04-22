import time
from celery import Celery

app = Celery('tasks', broker='redis://localhost')


@app.task
def import_musicxml_files(replace_data=False):
    for x in range(100):
        print(x)
        time.sleep(10)
