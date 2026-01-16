import pandas as pd
from datetime import date, timedelta
import os
from tqdm import tqdm


def combine_all_descending_quantity_data(start_date: date, end_date: date, output_path: str, to_csv: bool = False):
    all_data = []

    total_days = (end_date - start_date).days + 1
    current_date = start_date

    with tqdm(total=total_days, desc="Processing") as pbar:
        while current_date <= end_date:
            month = f"{current_date.month:02d}"
            day = f"{current_date.day:02d}"
            formatted_date = month + day
            INPUT_FOLDER = f"bid_info/sorted/highest_quantity/descending_quantity/month_{month}"
            INPUT_FILE = os.path.join(INPUT_FOLDER, f"2025{formatted_date}_DESCENDING_QUANTITY.csv")

            if os.path.isfile(INPUT_FILE):
                df = pd.read_csv(INPUT_FILE)
                df['Date'] = formatted_date
                all_data.append(df)
            else:
                print(f"File {INPUT_FILE} does not exist.")

            current_date += timedelta(days=1)
            pbar.update(1)

    print(f"Finished adding all data. There are {len(all_data)} files added.")
    print(f"---------Now combining the files... -----------")

    ful_df = pd.concat(all_data, ignore_index=True)
    df_reordered = ful_df.sort_values(['RESOURCEBID_SEQ', 'Date'])

    if to_csv:
        df_reordered.to_csv(output_path, index=False)
        print(f"Successfully combined the data into a csv file in {output_path}.")
    return df_reordered


def count_quantity_occurrences(input_path: str, output_path: str, to_csv: bool = False):
    df = pd.read_csv(input_path)
    df_count = df.groupby(['RESOURCEBID_SEQ', 'SCH_BID_XAXISDATA']).size().reset_index(name='Count')
    df_count_sorted = df_count.sort_values(
        by=['SCH_BID_XAXISDATA', 'Count'],
        ascending=[False, False]
    )
    if to_csv:
        df_count_sorted.to_csv(output_path, index=False)
        print(f"Successfully write the count quantity occurrences to {output_path}.")
    return df_count_sorted


def count_quantity_occurrences_keep_core_info(input_path: str, output_path: str, to_csv: bool = False):
    df = pd.read_csv(input_path)
    df_count = df.groupby(['RESOURCEBID_SEQ', 'SCH_BID_XAXISDATA']).size().reset_index(name='Count')
    df_with_count = df.merge(
        df_count,
        on=['RESOURCEBID_SEQ', 'SCH_BID_XAXISDATA'],
        how='left'
    )

    df_with_count['Group_Max_Quantity'] = df_with_count.groupby('RESOURCEBID_SEQ')['SCH_BID_XAXISDATA'].transform('max')

    df_count_sorted = df_with_count.sort_values(
        by=['Group_Max_Quantity', 'RESOURCEBID_SEQ', 'SCH_BID_XAXISDATA', 'Count'],
        ascending=[False, False, False, False]
    )

    df_count_sorted = df_count_sorted.drop(columns=['Group_Max_Quantity'])
    
    if to_csv:
        df_count_sorted.to_csv(output_path, index=False)
        print(f"Successfully write the count quantity occurrences to {output_path}.")
    return df_count_sorted


def keep_only_resource_type(input_path: str, output_path: str, mask: str, to_csv: bool = False):
    df = pd.read_csv(input_path)
    df_mask = df['RESOURCE_TYPE'] == mask
    df_masked = df[df_mask]
    if to_csv:
        df_masked.to_csv(output_path, index=False)
        print(f"Successfully kept {mask} relevant data to {output_path}.")
    return df_masked


def keep_unique_quantity_rows(input_path: str, output_path: str, to_csv: bool = False):
    df = pd.read_csv(input_path)
    subset_cols = ['RESOURCEBID_SEQ', 'SCH_BID_XAXISDATA']
    df_unique = df.drop_duplicates(
        subset=subset_cols, 
        keep='first'
    )
    # 'STARTTIME', 
    df_cleaned = df_unique.drop(['Date'], axis=1)
    if to_csv:
        df_cleaned.to_csv(output_path, index=False)
        print(f"Successfully kept unique quantity rows. Output to {output_path}.")
    return df_cleaned


if __name__ == "__main__":  
    start_date = date(2025, 1, 1)
    end_date = date(2025, 8, 14)

    OUTPUT_PATH_COMBINED = f"bid_info/sorted/highest_quantity/descending_quantity/COMBINED_{start_date}_to_{end_date}.csv"
    combine_all_descending_quantity_data(start_date, end_date, OUTPUT_PATH_COMBINED, True)

    INPUT_PATH = f"bid_info/sorted/highest_quantity/descending_quantity/COMBINED_{start_date}_to_{end_date}.csv"
    OUTPUT_PATH = f"bid_info/sorted/highest_quantity/descending_quantity/COUNT_QUANTITY_SORTED_{start_date}_to_{end_date}.csv"
    df_count_sorted = count_quantity_occurrences_keep_core_info(INPUT_PATH, OUTPUT_PATH, True)

    unique_resource_id = df_count_sorted['RESOURCEBID_SEQ'].nunique()
    print(f"There are {unique_resource_id} unique resource id's.")

    MASK = "GENERATOR"
    MASK_ONLY_OUTPUT_PATH = f"bid_info/sorted/highest_quantity/descending_quantity/COUNT_QUANTITY_SORTED_{MASK}_{start_date}_to_{end_date}.csv"
    keep_only_resource_type(OUTPUT_PATH, MASK_ONLY_OUTPUT_PATH, MASK, True)

    UNIQUE_OUTPUT_PATH = f"bid_info/sorted/highest_quantity/descending_quantity/COUNT_QUANTITY_SORTED_{MASK}_UNIQUE_{start_date}_to_{end_date}.csv"
    keep_unique_quantity_rows(MASK_ONLY_OUTPUT_PATH, UNIQUE_OUTPUT_PATH, True)