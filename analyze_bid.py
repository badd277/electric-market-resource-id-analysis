import csv
import pandas as pd
import matplotlib.pyplot as plt

# for start_time, sub in df.groupby("STARTTIME"):
#     print(start_time, len(sub))
#     x = sub["SCH_BID_XAXISDATA"]
#     y = sub["SCH_BID_Y1AXISDATA"]
#     plt.plot(x, y, label=start_time, marker="o")


def extract_bid_data_for_generator(bid_seq: str, gen_id: int):
    df = pd.read_csv(bid_seq)
    mask_for_gen_id = df["RESOURCEBID_SEQ"] == gen_id
    df = df[mask_for_gen_id]
    return df


def plot_bid_data_for_generator(df: pd.DataFrame, gen_id: int, start_time: str, product_type: str = "EN"):
    figsize = (10, 10)
    plt.figure(figsize=figsize)

    mask_start_time = df["STARTTIME"] == start_time
    mask_product_type = df["MARKETPRODUCTTYPE"] == product_type
    df = df[mask_start_time & mask_product_type]

    df_sorted = df.sort_values("SCH_BID_XAXISDATA", ascending=True)
    x = df_sorted["SCH_BID_XAXISDATA"]
    y = df_sorted["SCH_BID_Y1AXISDATA"]

    plt.plot(x, y, label=start_time, marker="o")
    plt.title(f"Bid Curves for RESOURCEBID_SEQ {gen_id}")
    plt.xlabel("Quantity (MW)")
    plt.ylabel("Bid Price ($/MWh)")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    MONTH = "07"
    DAY = "13"
    BID_ID = 394840

    FILE_INPUT = f"bid_info/files/2025{MONTH}{DAY}_2025{MONTH}{DAY}_PUB_BID_DAM_v3.csv"
    print(FILE_INPUT)
    OUTPUT = f"bid_info/results/2025{MONTH}{DAY}_result_RESOURCEBID_SEQ_{BID_ID}.csv"

    start_time = f"2025-{MONTH}-{DAY}T00:00:00"
    print(start_time)

    df = extract_bid_data_for_generator(FILE_INPUT, BID_ID)
    plot_bid_data_for_generator(df, BID_ID, start_time)