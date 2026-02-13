from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pytz
from scraper import scrape_all_pages, upload_to_postgres


def etl_task():
    # Scrape data from all pages
    df = scrape_all_pages(start=1, end=412)

    # Upload data to PostgreSQL
    upload_to_postgres(
        df=df,
        host='postgres',
        database='books_db',
        table_name='books',
        username='books_user',
        password='books_password',
        port=5432
    )

baku_tz = pytz.timezone("Asia/Baku")

with DAG(
    dag_id="alinino_scraper_dag",
    start_date=datetime(2026, 2, 5, tzinfo=baku_tz),
    schedule_interval="0 6 * * *",  # 6:00 AM Baku time
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5)
    },
    tags=["scraper", "alinino"]
) as dag:

    run_etl = PythonOperator(
        task_id="scrape_and_upload",
        python_callable=etl_task
    )