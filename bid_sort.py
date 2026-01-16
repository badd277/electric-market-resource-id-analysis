import pandas as pd
from datetime import date, timedelta
import os

def find_highest_bid_id(bid_seq: str) -> pd.DataFrame:
    if os.path.isfile(bid_seq):
        df = pd.read_csv(bid_seq)

        df["max_bid"] = df.groupby('RESOURCEBID_SEQ')['SCH_BID_Y1AXISDATA'].transform('max')

        df_sorted = df.sort_values(['max_bid', 'SCH_BID_Y1AXISDATA'], scending=[False, False])

        return df_sorted
    else:
        return None



def find_highest_quantity_id(bid_seq: str) -> pd.DataFrame:
    if os.path.isfile(bid_seq):
        df = pd.read_csv(bid_seq)
        df["highest_quantity"] = df.groupby('RESOURCEBID_SEQ')['SCH_BID_XAXISDATA'].transform('max')

        df_sorted = df.sort_values(['highest_quantity', 'SCH_BID_XAXISDATA'], ascending=[False, False])
        return df_sorted
    else:
        return None


def get_resource_id_descending_highest_quantity(bid_seq: str):
    if os.path.isfile(bid_seq):
        df = pd.read_csv(bid_seq)
        idx = df.groupby('RESOURCEBID_SEQ')['SCH_BID_XAXISDATA'].idxmax()
        idx = idx.dropna()
        df_max_rows = df.loc[idx]
        df_core = select_core_info(df_max_rows)
        df_sorted = df_core.sort_values(['SCH_BID_XAXISDATA'], ascending=[False])
        # print(df_sorted)
        return df_sorted
    else:
        return None


def select_core_info(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_select = ['STARTTIME', 'RESOURCE_TYPE', 'RESOURCEBID_SEQ', 
                         'MARKETPRODUCTTYPE', 'SCH_BID_XAXISDATA', 'SCH_BID_Y1AXISDATA']
    return df[columns_to_select]



if __name__ == "__main__":    
    start_date = date(2025, 1, 1)
    end_date = date(2025, 8, 14)

    current_date = start_date

    while current_date <= end_date:
        month = f"{current_date.month:02d}"
        day = f"{current_date.day:02d}"
        formatted_date = month + day

        print(f"Attempting to get data for resource id descending highest quantity for 2025_{formatted_date}...")

        INPUT_FOLDER = f"bid_info/files/month_{month}"
        INPUT_FILE = os.path.join(INPUT_FOLDER, f"2025{formatted_date}_2025{formatted_date}_PUB_BID_DAM_v3.csv")
        OUTPUT_FOLDER = f"bid_info/sorted/highest_quantity/descending_quantity/month_{month}"
        try:
            os.mkdir(OUTPUT_FOLDER)
            print(f"Directory {OUTPUT_FOLDER} created successfully.")
        except FileExistsError:
            print(f"Directory {OUTPUT_FOLDER} already exists.")
    
        OUTPUT = os.path.join(OUTPUT_FOLDER, f"2025{formatted_date}_DESCENDING_QUANTITY.csv")
        
        df_descending_highest_quantity = get_resource_id_descending_highest_quantity(INPUT_FILE)
        if df_descending_highest_quantity is not None:
            df_descending_highest_quantity.to_csv(OUTPUT, index=False)
        else:
            print(f"Skipping {INPUT_FILE} since result is None.")

        current_date += timedelta(days=1)
