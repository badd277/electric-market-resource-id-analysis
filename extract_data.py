from datetime import date, timedelta
import os
import zipfile


def extract_data(month: str, day: str):
    INPUT_FOLDER = f"bid_info/zipfiles/month_{month}"
    INPUT_FILE = os.path.join(INPUT_FOLDER, f"data_{month}{day}.zip")

    OUTPUT_FOLDER = f"bid_info/files/month_{month}"
    
    try:
        os.mkdir(OUTPUT_FOLDER)
        print(f"Directory {OUTPUT_FOLDER} created successfully.")
    except FileExistsError:
        print(f"Directory {OUTPUT_FOLDER} already exists.")

    
    try:
        with zipfile.ZipFile(INPUT_FILE, 'r') as zf:
            zf.extractall(OUTPUT_FOLDER)
        print(f"Successfully extracted {INPUT_FILE} to {OUTPUT_FOLDER}.")
    except zipfile.BadZipFile:
        print(f"Error: '{INPUT_FILE}' is not a valid zip file.")
    except FileNotFoundError:
        print(f"Error: Zip file not found at '{INPUT_FILE}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    start_date = date(2025, 1, 1)
    end_date = date(2025, 8, 14)

    current_date = start_date

    while current_date <= end_date:
        month = f"{current_date.month:02d}"
        day = f"{current_date.day:02d}"
        formatted_date = month + day
        print(f"Attempting to extract data for 2025_{formatted_date}...")
        extract_data(month, day)
        current_date += timedelta(days=1)