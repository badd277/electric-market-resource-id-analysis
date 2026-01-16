from datetime import date, timedelta

start_date = date(2025, 1, 1)
end_date = date(2025, 8, 14)

date_difference = (end_date - start_date).days + 1

print(f"There are {date_difference} days from {start_date} to {end_date}.")