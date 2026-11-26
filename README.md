
# Population Data Analyzer

A menu-driven Python console program that reads city population records from a CSV file, cleans them, and shows a summary and two charts.

Project for *Programming Fundamentals and Logic Building Using Python*, Rungta International Skills University, Bhilai (Session 2026-27).

## Features

- Reads `population.csv` with the columns `City`, `Year` and `Population`
- Validates and cleans the data, and tells you about every change it makes:
  - trims extra spaces from city names
  - skips rows with an empty city, a non-whole-number year, or a population that is not greater than zero
  - removes exact duplicate rows
  - keeps the last row when a city appears twice in the same year
- Prints a summary for the latest year: total population and largest city
- Calculates each city's percentage growth and names the fastest-growing city
- Shows a population growth bar chart and a population trend line chart
- Handles a missing file, a missing column and empty data with a clear message instead of crashing

## Requirements

- Python 3.9 or newer (tested on Python 3.12.3)
- pandas (tested with 3.0.6)
- matplotlib (tested with 3.11.2)

```bash
pip install pandas matplotlib
```

## Files

| File | Description |
|---|---|
| `population_data_analyzer.py` | The complete program |
| `population.csv` | Input data |

## Input format

Place `population.csv` in the same folder as the script.

```csv
City,Year,Population
Raipur,2020,1000000
Raipur,2024,1100000
Durg,2020,500000
Durg,2024,600000
```

## How to run

```bash
python population_data_analyzer.py
```

Menu:

```
Choose an option:
1. Show summary
2. Show population growth chart
3. Show population trend chart
4. Exit
```

| Option | What it does |
|---|---|
| 1 | Prints the latest-year summary and growth by city |
| 2 | Prints the same summary, then shows the growth bar chart |
| 3 | Shows the population trend line chart |
| 4 | Exits the program |

## Sample output

With the sample data above, option 1 prints:

```
Summary for 2024
Total population: 1700000
Largest city: Raipur (1100000)

Growth by city:
Durg: +20.00%
Raipur: +10.00%

Fastest growing: Durg (+20.00%)
```

## How growth is calculated

Growth is measured from each city's earliest year to its latest year:

```
Growth % = (latest population - earliest population) / earliest population * 100
```

A city needs data for at least two different years to have a growth value.

## Program structure

| Function | Purpose |
|---|---|
| `load_population_data()` | Reads the CSV, validates and cleans it; returns a DataFrame, or `None` on failure |
| `show_summary(data)` | Prints the latest-year summary and growth; returns the growth results |
| `show_growth_chart(growth_results)` | Draws the growth bar chart |
| `show_population_trend_chart(data)` | Draws one trend line per city |
| `main()` | Loads the data once and runs the menu loop |

## Limitations

- Growth is the total change between the earliest and latest year, not a yearly rate, so cities covering different time spans are not directly comparable.
- The summary uses only the latest year; a city with no record in that year is left out of the total and largest-city check.
- Charts are displayed on screen and are not saved to files.
- The CSV file name is fixed in the script (`CSV_FILE`).

## Possible improvements

- Compound annual growth rate (CAGR)
- Choose a year or year range, and the CSV path, at run time
- Save charts as images and export the summary
- Automated unit tests
