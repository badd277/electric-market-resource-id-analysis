# Electricity Market - Resource ID Analysis

## Purpose
- Analyze CAISO DAM bids to
  - extract each resource’s max hourly bid by day,
  - count bidding frequency across a date range, and
  - compare max bid quantity to NQC report to help map RESOURCEBID_SEQ to physical generators.

## How to use
1. Download (define a date range): `get_oasis_bid_data.py`
2. Extract files: `extract_data.py`
3. Combine across dates: `analyze_max_quantity.py`
4. Analyze NQC report: `analyzing_nqc_reports.py`
5. Plot: `analyze_bid.py`
6. Extra utilities: `sum_count.py`, `date_calculation.py`

## Files
- **Get_oasis_bid_data.py** — Downloads CAISO DAM bid zips into folders.
- **Extract_data.py** — Unzips the downloaded files into files/month folders.
- **Bid_sort.py** — For each day, find each resource id’s quantity row and keep relevant core fields. Writes to a csv file.
- **Analyze_max_quantity.py** — Combines the max quantity across a date range for all the resource id’s. Counts the occurrences of the same max quantity and writes to the “Count” column.
- **Analyzing_nqc_reports.py** — Loads the NQC report, computes each generator’s yearly max. Outputs an xlsx file.
- **Analyze_bid.py** — Filters a day’s bid file to a resource id and plots its bid curve.
- **Sum_count.py** — Sums up the counts within a time window.
- **Date_calculation.py** — Computes number of days between two dates (to bound loops).

## Notes
- The scripts extract each day’s max energy bid (MW) for every RESOURCEBID_SEQ (resource id) across a date range.
- Summing the daily counts per resource id gives the number of days that sequence submitted a bid in that window.
  - Example: 01/01/2025–08/14/2025 has 226 days; a total count of 226 means the resource id bids every day in the range.
- However, this does not give conclusive evidence that the resource id’s that bids everyday has the same resource id across that range.
- The max bid quantity data could be useful. In principle, the max bid data should not exceed the nameplate capacity of the generator.
- The NQC report contains the deliverable capacity that must be available. It was used as a reference to compare with the max bid quantity, since the max bid quantity could be close to the net qualifying capacity. By comparing each sequence’s max bid quantity with the Yearly_Max column of the outputted NQC report, you can often match a resource id to a specific generator name with more confidence.
