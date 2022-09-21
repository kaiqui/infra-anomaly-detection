from celery import Celery
from utils.config.settings import BROKER, DB_CONN


app = Celery('aipo',
             broker=BROKER,
             backend=DB_CONN,
             include=['task.predict'])


app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()