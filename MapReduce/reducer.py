#!/usr/bin/env python3
import sys

# Initialize variables for the current year and the highest temperature
current_year = None
max_temperature = None

# Read input line by line
for line in sys.stdin:
    line = line.strip()
    
    # Parse the input (year, temperature)
    year, temperature = line.split('\t')
    temperature = int(temperature)
    
    # If the year has changed, print the max temperature for the previous year
    if current_year and current_year != year:
        print(f"{current_year}\t{max_temperature}")
        max_temperature = temperature
    
    # Update the max temperature for the current year
    if current_year != year:
        current_year = year
        max_temperature = temperature
    else:
        max_temperature = max(max_temperature, temperature)

# Output the last year's maximum temperature
if current_year:
    print(f"{current_year}\t{max_temperature}")
