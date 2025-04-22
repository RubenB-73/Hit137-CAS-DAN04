import os
import csv
from collections import defaultdict

# Folder containing CSVs
data_directory = "C:\\Users\\Smit Pc\\Desktop\\Current ASiignrmnts\\temperature_data"

# Output file destinations 
output_folder = "C:\\Users\\Smit Pc\\Desktop\\Current ASiignrmnts"
average_seasonal_temps_file = os.path.join(output_folder, "average_temp.txt")
temp_range_extremes_file = os.path.join(output_folder, "largest_temp_range_station.txt")
hottest_coldest_stations_file = os.path.join(output_folder, "warmest_and_coolest_station.txt")

# Mapping of seasons to their respective months
seasonal_month_map = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

# Storage for aggregated seasonal data and individual station readings
seasonal_data_points = defaultdict(list)
station_monthly_readings = {}

problematic_data_entries = 0

for file in os.listdir(data_directory):
    if file.startswith("stations_group_") and file.endswith(".csv"):
        full_file_path = os.path.join(data_directory, file)
        with open(full_file_path, newline='') as csv_document:
            data_reader = csv.DictReader(csv_document)
            for entry_number, record in enumerate(data_reader, 1):
                try:
                    weather_station = record["STATION_NAME"].strip()
                    monthly_temperatures = []

                    for month_name in [
                        "January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"
                    ]:
                        value = record[month_name].strip()
                        temperature_value = float(value) if value else None
                        if temperature_value is not None:
                            monthly_temperatures.append(temperature_value)

                    # Storing monthly temperatures for each station
                    station_monthly_readings[weather_station] = monthly_temperatures

                    # Grouping data by season
                    for current_season, months_in_season in seasonal_month_map.items():
                        for month_name in months_in_season:
                            value = record.get(month_name, "").strip()
                            if value:
                                seasonal_data_points[current_season].append(float(value))
                except Exception as error_detail:
                    problematic_data_entries += 1
                    print(f"Issue encountered in file: {file}, at row: {entry_number}. Details: {error_detail}")

# Step 1: Outputting average seasonal temperatures
with open(average_seasonal_temps_file, "w") as output_file:
    output_file.write("Average Temperatures Across Seasons (°C):\n")
    for season_label in ["Summer", "Autumn", "Winter", "Spring"]:
        temps = seasonal_data_points[season_label]
        if temps:
            average_temp = sum(temps) / len(temps)
            output_file.write(f"{season_label}: {average_temp:.2f}\n")
        else:
            output_file.write(f"{season_label}: Data currently unavailable.\n")

# Step 2: Identifying station(s) with the most extreme temperature variation
max_temp_spread = 0
stations_with_max_spread = []

for station_name, temps in station_monthly_readings.items():
    if temps:
        temp_spread = max(temps) - min(temps)
        if temp_spread > max_temp_spread:
            max_temp_spread = temp_spread
            stations_with_max_spread = [station_name]
        elif temp_spread == max_temp_spread:
            stations_with_max_spread.append(station_name)

with open(temp_range_extremes_file, "w") as output_file:
    output_file.write(f"Largest Temperature Range Observed: {max_temp_spread:.2f}°C\n")
    output_file.write("Station(s) Exhibiting This Range:\n")
    for station in stations_with_max_spread:
        output_file.write(f"{station}\n")

# Step 3: Determining the stations with the highest and lowest average temperatures
highest_average_temp = float("-inf")
lowest_average_temp = float("inf")
hottest_stations = []
coldest_stations = []

for station_name, temps in station_monthly_readings.items():
    if temps:
        average_temp_station = sum(temps) / len(temps)
        if average_temp_station > highest_average_temp:
            highest_average_temp = average_temp_station
            hottest_stations = [station_name]
        elif average_temp_station == highest_average_temp:
            hottest_stations.append(station_name)

        if average_temp_station < lowest_average_temp:
            lowest_average_temp = average_temp_station
            coldest_stations = [station_name]
        elif average_temp_station == lowest_average_temp:
            coldest_stations.append(station_name)

with open(hottest_coldest_stations_file, "w") as output_file:
    output_file.write(f"Highest Average Temperature: {highest_average_temp:.2f}°C\n")
    output_file.write("Warmest Station(s):\n")
    for station in hottest_stations:
        output_file.write(f"{station}\n")

    output_file.write(f"\nLowest Average Temperature: {lowest_average_temp:.2f}°C\n")
    output_file.write("Coolest Station(s):\n")
    for station in coldest_stations:
        output_file.write(f"{station}\n")

print(f"Processing complete! {problematic_data_entries} data entries encountered issues during analysis.")