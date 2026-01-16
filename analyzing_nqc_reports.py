import pandas as pd

def sort_based_on_largest_capacity(input_file: str, output_file: str, to_excel: bool = False):
    df = pd.read_excel(input_file, index_col=0, sheet_name=1)
    month_cols = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    df['Yearly_Max'] = df[month_cols].max(axis=1)
    df_sorted = df.sort_values(['Yearly_Max'],ascending=[False])
    df_sorted.drop(columns=['Yearly_Max'])
    if to_excel:
        df_sorted.to_excel(output_file, index=False)
        print(f"Successfully sorted based on largest capacity and saved to {output_file}")
    return df_sorted



if __name__ == "__main__":  
    INPUT = "net_qualifying_capacity_reports/final-net-qualifying-capacity-report-for-compliance-year-2024.xlsx"
    OUTPUT = "net_qualifying_capacity_reports/results/NQC_2024_sorted.xlsx"

    sort_based_on_largest_capacity(INPUT, OUTPUT, True)