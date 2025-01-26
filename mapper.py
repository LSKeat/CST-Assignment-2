#!/usr/bin/env python3
import sys

# Read each line of input
for line in sys.stdin:
    line = line.strip()
    try:
        tokens = line.split()
        if len(tokens) >= 2:
            year = tokens[0]  # First token is the year
            temperature = int(tokens[1].strip())  # Second token is the temperature

            # Emit key-value pair: year as key, temperature as value
            print(f"{year}\t{temperature}")
    except ValueError:
        pass  # Ignore lines with invalid temperature
