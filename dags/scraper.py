from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd
import time
from sqlalchemy import create_engine, text

def scrape_page_eng(page: int):
    if page == 1:
        url = "https://alinino.az/collection/knigi-na-angliyskom-yazyke"
    else:
        url = f"https://alinino.az/collection/knigi-na-angliyskom-yazyke?page={page}"

    response = rq.get(url, timeout=10)
    response.raise_for_status()

    soup = bs(response.text, "html.parser")

    names = soup.find_all("a", class_="product-card__title")
    prices = soup.find_all("span", class_="product-card__price")
    # old_prices = soup.find_all("span", class_="product-card__old-price")

    data = []

    for i in range(len(names)):
        name = names[i].text.strip()

        price_parts = prices[i].text.strip().split()
        current_price = price_parts[0]
        currency = price_parts[1] if len(price_parts) > 1 else None

        # # Old price may be missing
        # old_price = (
        #     old_prices[i].text.strip().split()[0]
        #     if i < len(old_prices)
        #     else None
        # )

        data.append({
            "Product Name": name,
            "Current Price": current_price,
            #"Old Price": old_price,
            "Currency": currency
        })

    return pd.DataFrame(data)



def scrape_page_az(page: int):
    if page == 1:
        url = "https://alinino.az/collection/knigi-na-azerbaydzhanskom-yazyke"
    else:
        url = f"https://alinino.az/collection/knigi-na-azerbaydzhanskom-yazyke?page={page}"

    response = rq.get(url, timeout=10)
    response.raise_for_status()

    soup = bs(response.text, "html.parser")

    names = soup.find_all("a", class_="product-card__title")
    prices = soup.find_all("span", class_="product-card__price")
    # old_prices = soup.find_all("span", class_="product-card__old-price")

    data = []

    for i in range(len(names)):
        name = names[i].text.strip()

        price_parts = prices[i].text.strip().split()
        current_price = price_parts[0]
        currency = price_parts[1] if len(price_parts) > 1 else None

        # # Old price may be missing
        # old_price = (
        #     old_prices[i].text.strip().split()[0]
        #     if i < len(old_prices)
        #     else None
        # )

        data.append({
            "Product Name": name,
            "Current Price": current_price,
            #"Old Price": old_price,
            "Currency": currency
        })

    return pd.DataFrame(data)



def scrape_page_rus(page: int):
    if page == 1:
        url = "https://alinino.az/collection/knigi-na-russkom-yazyke"
    else:
        url = f"https://alinino.az/collection/knigi-na-russkom-yazyke?page={page}"

    response = rq.get(url, timeout=10)
    response.raise_for_status()

    soup = bs(response.text, "html.parser")

    names = soup.find_all("a", class_="product-card__title")
    prices = soup.find_all("span", class_="product-card__price")
    # old_prices = soup.find_all("span", class_="product-card__old-price")

    data = []

    for i in range(len(names)):
        name = names[i].text.strip()

        price_parts = prices[i].text.strip().split()
        current_price = price_parts[0]
        currency = price_parts[1] if len(price_parts) > 1 else None

        # # Old price may be missing
        # old_price = (
        #     old_prices[i].text.strip().split()[0]
        #     if i < len(old_prices)
        #     else None
        # )

        data.append({
            "Product Name": name,
            "Current Price": current_price,
            #"Old Price": old_price,
            "Currency": currency
        })

    return pd.DataFrame(data)



def scrape_page_turk(page: int):
    if page == 1:
        url = "https://alinino.az/collection/knigi-na-turetskom-yazyke"
    else:
        url = f"https://alinino.az/collection/knigi-na-turetskom-yazyke?page={page}"

    response = rq.get(url, timeout=10)
    response.raise_for_status()

    soup = bs(response.text, "html.parser")

    names = soup.find_all("a", class_="product-card__title")
    prices = soup.find_all("span", class_="product-card__price")
    # old_prices = soup.find_all("span", class_="product-card__old-price")

    data = []

    for i in range(len(names)):
        name = names[i].text.strip()

        price_parts = prices[i].text.strip().split()
        current_price = price_parts[0]
        currency = price_parts[1] if len(price_parts) > 1 else None

        # # Old price may be missing
        # old_price = (
        #     old_prices[i].text.strip().split()[0]
        #     if i < len(old_prices)
        #     else None
        # )

        data.append({
            "Product Name": name,
            "Current Price": current_price,
            #"Old Price": old_price,
            "Currency": currency
        })

    return pd.DataFrame(data)




def scrape_all_pages_eng(start=1, end=412):
    all_data = []

    for page in range(start, end + 1):
        df = scrape_page_eng(page)
        all_data.append(df)

        time.sleep(3)  # break for a second

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.index += 1
    return final_df



def scrape_all_pages_az(start=1, end=145):
    all_data = []

    for page in range(start, end + 1):
        df = scrape_page_az(page)
        all_data.append(df)

        time.sleep(3)  # break for a second

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.index += 1
    return final_df



def scrape_all_pages_rus(start=1, end=712):
    all_data = []

    for page in range(start, end + 1):
        df = scrape_page_rus(page)
        all_data.append(df)

        time.sleep(3)  # break for a second

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.index += 1
    return final_df



def scrape_all_pages_turk(start=1, end=190):
    all_data = []

    for page in range(start, end + 1):
        df = scrape_page_turk(page)
        all_data.append(df)

        time.sleep(3)  # break for a second

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.index += 1
    return final_df




def upload_to_postgres(
    df: pd.DataFrame,
    host: str,
    database: str,
    table_name: str,
    username: str,
    password: str,
    port: int = 5432
):
    connection_string = (
        f"postgresql+psycopg2://{username}:{password}"
        f"@{host}:{port}/{database}"
    )

    engine = create_engine(connection_string)

    with engine.begin() as conn:
        # Drop table if exists
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name};"))

        # Create & insert
        df.to_sql(
            table_name,
            con=conn,
            index=False,
            if_exists="replace"
        )

    print(f"Table '{table_name}' uploaded successfully.")
