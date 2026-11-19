# Import pandas for reading and cleaning the CSV data.
import pandas as pd

# Import matplotlib for creating charts.
import matplotlib.pyplot as plt


# Store the CSV file name in one place so it is easy to change.
CSV_FILE = "population.csv"


def load_population_data():
    """Read the CSV file and clean its data."""

    # Try to open the CSV file. Show a message if it cannot be found or read.
    try:
        data = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"Could not find {CSV_FILE}. Put it beside this Python file.")
        return None
    except Exception as error:
        print(f"Could not read the CSV file: {error}")
        return None

    # Make sure the CSV has all the columns this program needs.
    required_columns = {"City", "Year", "Population"}
    if not required_columns.issubset(data.columns):
        print("The CSV needs these columns: City, Year, Population")
        return None

    # Remove extra spaces from city names and convert year/population to numbers.
    data["City"] = data["City"].astype("string").str.strip()
    data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
    data["Population"] = pd.to_numeric(data["Population"], errors="coerce")

    # Mark rows as valid when they have a city, a whole-number year,
    # and a population greater than zero.
    valid_rows = (
        data["City"].notna()
        & data["City"].ne("")
        & data["Year"].notna()
        & data["Population"].notna()
        & data["Year"].mod(1).eq(0)
        & data["Population"].gt(0)
    )

    # Tell the user which rows were skipped.
    for row_number in data.index[~valid_rows]:
        print(
            f"Row {row_number + 2} skipped: "
            "invalid city, year, or population."
        )

    # Keep only valid rows and use integer types for year and population.
    data = data.loc[valid_rows].copy()
    data["Year"] = data["Year"].astype(int)
    data["Population"] = data["Population"].astype(int)

    # Remove rows that are exact duplicates.
    rows_before = len(data)
    data = data.drop_duplicates()
    exact_duplicates = rows_before - len(data)

    if exact_duplicates:
        print(f"Removed {exact_duplicates} exact duplicate row(s).")

    # If a city appears more than once in the same year, keep the last row.
    rows_before = len(data)
    data = data.drop_duplicates(subset=["City", "Year"], keep="last")
    repeated_entries = rows_before - len(data)

    if repeated_entries:
        print(
            f"Removed {repeated_entries} repeated city/year row(s); "
            "kept the last one."
        )

    # Stop if no usable rows remain.
    if data.empty:
        print("There are no valid rows to show.")
        return None

    # Return the cleaned data to the rest of the program.
    return data


def show_summary(data):
    """Print a summary for the latest year and calculate city growth."""

    # Find the latest year and select its rows.
    latest_year = data["Year"].max()
    latest_data = data[data["Year"] == latest_year]

    # Calculate the total population and find the largest city.
    total_population = latest_data["Population"].sum()
    largest_city_row = latest_data.loc[latest_data["Population"].idxmax()]

    # Print the summary information.
    print(f"\nSummary for {latest_year}")
    print(f"Total population: {total_population}")
    print(
        f"Largest city: {largest_city_row['City']} "
        f"({largest_city_row['Population']})"
    )

    # Create a list to store growth results for cities with multiple years.
    growth_results = []

    # Calculate growth from each city's earliest year to its latest year.
    for city, city_data in data.groupby("City"):
        city_data = city_data.sort_values("Year")

        # Growth needs at least two different years of data.
        if city_data["Year"].nunique() < 2:
            continue

        earliest_population = city_data.iloc[0]["Population"]
        latest_population = city_data.iloc[-1]["Population"]

        # Calculate percentage growth from the earliest to latest value.
        growth_percent = (
            (latest_population - earliest_population)
            / earliest_population
            * 100
        )

        # Save the city's name and growth percentage.
        growth_results.append({
            "City": city,
            "Growth": growth_percent,
        })

    # Explain when there is not enough data to calculate growth.
    if not growth_results:
        print("Growth is unavailable: each city needs data for two years.")
        return []

    # Print the growth percentage for each city.
    print("\nGrowth by city:")
    for result in growth_results:
        print(f"{result['City']}: {result['Growth']:+.2f}%")

    # Find and print the city with the highest growth percentage.
    fastest_growing = max(growth_results, key=lambda item: item["Growth"])
    print(
        f"\nFastest growing: {fastest_growing['City']} "
        f"({fastest_growing['Growth']:+.2f}%)"
    )

    # Return growth values so the growth chart can use them.
    return growth_results


def show_growth_chart(growth_results):
    """Display a bar chart comparing population growth by city."""

    # A growth chart needs at least one city with data for two years.
    if not growth_results:
        print("Growth chart unavailable: there is not enough year data.")
        return

    # Convert the growth list to a DataFrame and sort it for easier reading.
    growth_data = pd.DataFrame(growth_results).sort_values("Growth")

    # Create and label the bar chart.
    plt.figure(figsize=(8, 5))
    plt.bar(growth_data["City"], growth_data["Growth"], color="steelblue")
    plt.title("Population Growth by City")
    plt.xlabel("City")
    plt.ylabel("Growth (%)")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Display this chart in its own figure.
    plt.show()


def show_population_trend_chart(data):
    """Display a line chart of population over time for each city."""

    # Start a separate figure for the population trend chart.
    plt.figure(figsize=(8, 5))

    # Draw one line for each city, with years in chronological order.
    for city, city_data in data.groupby("City"):
        city_data = city_data.sort_values("Year")
        plt.plot(
            city_data["Year"],
            city_data["Population"],
            marker="o",
            label=city,
        )

    # Add the chart title, axis labels, legend, and grid.
    plt.title("Population Trend by City")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.legend(title="City")
    plt.grid(True)
    plt.tight_layout()

    # Display this chart in its own figure.
    plt.show()


def main():
    """Load the data and display the four-option menu."""

    # Load and clean the CSV before showing the menu.
    data = load_population_data()

    # Stop the program if the CSV could not be loaded or has no valid data.
    if data is None:
        return

    # Keep showing the menu until the user chooses Exit.
    while True:
        print("\nChoose an option:")
        print("1. Show summary")
        print("2. Show population growth chart")
        print("3. Show population trend chart")
        print("4. Exit")

        # Read the user's menu choice.
        choice = input("Type 1, 2, 3, or 4: ").strip()

        # Run the summary option.
        if choice == "1":
            show_summary(data)

        # Calculate growth, then show the growth chart.
        elif choice == "2":
            growth_results = show_summary(data)
            show_growth_chart(growth_results)

        # Show the population trend chart.
        elif choice == "3":
            show_population_trend_chart(data)

        # Exit the menu and end the program.
        elif choice == "4":
            print("Goodbye!")
            break

        # Tell the user when their choice is not one of the four options.
        else:
            print("Invalid choice. Please type 1, 2, 3, or 4.")


# Start the program when this file is run directly.
if __name__ == "__main__":
    main()
