import pandas as pd
from datetime import date

# add up count for each resource id

start_date = date(2025, 1, 1)
end_date = date(2025, 8, 14)

INPUT = f"bid_info/sorted/highest_quantity/descending_quantity/COUNT_QUANTITY_SORTED_GENERATOR_UNIQUE_{start_date}_to_{end_date}.csv"
OUTPUT = f"bid_info/sorted/highest_quantity/descending_quantity/COUNT_SUM_{start_date}_to_{end_date}.csv"

df = pd.read_csv(INPUT)
count_sum = df.groupby("RESOURCEBID_SEQ")["Count"].sum()
max_bid_quantity = df.groupby("RESOURCEBID_SEQ")["SCH_BID_XAXISDATA"].max()
output = max_bid_quantity.to_frame().join(count_sum.to_frame(name="Count_Sum")).reset_index()
sorted = output.sort_values("SCH_BID_XAXISDATA", ascending=False)

sorted.to_csv(OUTPUT, index=False)
print(count_sum)