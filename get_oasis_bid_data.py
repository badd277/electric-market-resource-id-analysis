import requests
from datetime import date, timedelta
import os
import time


def get_oasis_bid_data(month: str, day: str):
    URL = f"https://oasis.caiso.com/oasisapi/GroupZip?resultformat=6&version=3&groupid=PUB_DAM_GRP&startdatetime=2025{month}{day}T07:00-0000"
    OUTPUT_folder = f"bid_info/zipfiles/month_{month}"
    filename = f"data_{month}{day}.zip"

    try:
        os.mkdir(OUTPUT_folder)
        print(f"Directory {OUTPUT_folder} created successfully.")
    except FileExistsError:
        print(f"Directory {OUTPUT_folder} already exists.")
    
    OUTPUT_full_path = os.path.join(OUTPUT_folder, filename)
    print(f"Attempt to write to path: {OUTPUT_full_path}...")

    try:
        r = requests.get(url=URL, stream=True)
        r.raise_for_status()

        with open(OUTPUT_full_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


if __name__ == "__main__":
    # get_oasis_bid_data("01", "05")

    start_date = date(2025, 1, 1)
    end_date = date(2025, 8, 14)

    current_date = start_date

    sec_to_sleep = 10

    while current_date <= end_date:
        month = f"{current_date.month:02d}"
        day = f"{current_date.day:02d}"
        formatted_date = month + day
        print(f"Attempting to get data for 2025_{formatted_date}...")
        get_oasis_bid_data(month, day)

        print(f"Sleeping for {sec_to_sleep} sec.")
        time.sleep(sec_to_sleep)

        current_date += timedelta(days=1)


