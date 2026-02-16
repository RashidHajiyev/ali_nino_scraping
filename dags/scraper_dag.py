from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.time_delta import TimeDeltaSensor
from datetime import datetime, timedelta
import pytz

from scraper import (
    scrape_all_pages_eng,
    scrape_all_pages_az,
    scrape_all_pages_rus,
    scrape_all_pages_turk,
    upload_to_postgres
)

# timezone
baku_tz = pytz.timezone("Asia/Baku")



def scrape_eng():
    df = scrape_all_pages_eng(start=1, end=412)
    upload_to_postgres(
        df=df,
        host='postgres',
        database='books_db',
        table_name='books_eng',
        username='books_user',
        password='books_password',
        port=5432
    )


def scrape_az():
    df = scrape_all_pages_az(start=1, end=145)
    upload_to_postgres(
        df=df,
        host='postgres',
        database='books_db',
        table_name='books_az',
        username='books_user',
        password='books_password',
        port=5432
    )


def scrape_rus():
    df = scrape_all_pages_rus(start=1, end=712)
    upload_to_postgres(
        df=df,
        host='postgres',
        database='books_db',
        table_name='books_rus',
        username='books_user',
        password='books_password',
        port=5432
    )


def scrape_turk():
    df = scrape_all_pages_turk(start=1, end=190)
    upload_to_postgres(
        df=df,
        host='postgres',
        database='books_db',
        table_name='books_turk',
        username='books_user',
        password='books_password',
        port=5432
    )


# ---------- DAG ----------

with DAG(
    dag_id="alinino_scraper_dag",
    start_date=datetime(2026, 2, 5, tzinfo=baku_tz),
    schedule_interval="0 6 * * *",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5)
    },
    tags=["scraper", "alinino"]
) as dag:

    task_eng = PythonOperator(
        task_id="scrape_eng",
        python_callable=scrape_eng
    )

    wait_1 = TimeDeltaSensor(
        task_id="wait_30min_after_eng",
        delta=timedelta(minutes=30)
    )

    task_az = PythonOperator(
        task_id="scrape_az",
        python_callable=scrape_az
    )

    wait_2 = TimeDeltaSensor(
        task_id="wait_30min_after_az",
        delta=timedelta(minutes=30)
    )

    task_rus = PythonOperator(
        task_id="scrape_rus",
        python_callable=scrape_rus
    )

    wait_3 = TimeDeltaSensor(
        task_id="wait_30min_after_rus",
        delta=timedelta(minutes=30)
    )

    task_turk = PythonOperator(
        task_id="scrape_turk",
        python_callable=scrape_turk
    )


    # ---------- PIPELINE ORDER ----------

    task_eng >> wait_1 >> task_az >> wait_2 >> task_rus >> wait_3 >> task_turk
