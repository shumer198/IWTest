import logging
import os

from celery import Celery
from celery.schedules import crontab

from models import (get_quotes_from_csv, get_quotes_with_seasonality,
                    load_quotes_to_db)
from settings import data_folder, file_name

celery = Celery()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls loader every 600 seconds.
    # sender.add_periodic_task(600.0, loader.s(), name='add every 600s')

    # Executes tuesday-saturday at 1:30 a.m.
    sender.add_periodic_task(
        crontab(hour=1, minute=30, day_of_week="2-6"),
        loader.s(),
    )


@celery.task
def loader():
    """
    Load quotes to database

    """
    file_path = os.path.join(data_folder, file_name)
    quotes = get_quotes_from_csv(file_path=file_path)
    quotes_with_seasonality = get_quotes_with_seasonality(quotes=quotes)
    load_quotes_to_db(quotes=quotes_with_seasonality)
