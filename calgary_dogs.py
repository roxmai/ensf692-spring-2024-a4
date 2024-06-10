import pandas as pd
import numpy as np

# calgary_dogs.py
# Roxanne Mai
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

def main():

    # Import data here
    try:
        df = pd.read_excel('CalgaryDogBreeds.xlsx')
    except FileNotFoundError:
        print("The data file 'CalgaryDogBreeds.xlsx' was not found.")
        return
    
    print("ENSF 692 Dogs of Calgary")

    # User input stage

    # Setting multi-index for the DataFrame
    df.set_index(['Year', 'Month', 'Breed'], inplace=True)

    breed = None
    while breed is None:
        try:
            # Prompt user for input
            user_input = input("Please enter a dog breed: ").strip().upper()
            # Check if the breed exists in the data
            if user_input not in df.index.get_level_values('Breed'):
                raise KeyError
            breed = user_input
        except KeyError:
            print("Dog breed not found in the data. Please try again.")
    
    # Data anaylsis stage    
    # Filtering data for the selected breed
    breed_data = df.xs(breed, level='Breed')

    # Find all years where the breed was listed
    years_listed = breed_data.index.get_level_values('Year').unique().tolist()
    print(f"The {breed} was found in the top breeds for years: {' '.join(map(str, years_listed))}")

    # Calculate total registrations for the breed
    total_registrations = breed_data['Total'].sum()
    print(f"There have been {total_registrations} {breed} dogs registered total.")

    # Calcuate yearly and total percentages
    year_totals = df.groupby(level='Year')['Total'].sum()
    breed_yearly_totals = breed_data.groupby(level='Year')['Total'].sum()
    
    for year in [2021, 2022, 2023]:
        year_total = year_totals.get(year, 0)
        breed_year_total = breed_yearly_totals.get(year, 0)
        
        if year_total != 0:
            percentage = (breed_year_total / year_total * 100) 
        else : 0
        print(f"The {breed} was {percentage:.6f}% of top breeds in {year}.")

    # Calculate percentage out of total three-year total
    three_year_total = year_totals.sum()
    if three_year_total != 0:
        percentage_total = (total_registrations / three_year_total * 100)
    else : 0
    print(f"The {breed} was {percentage_total:.6f}% of top breeds across all years.")

    # Find most popular months for the breed
    monthly_counts = breed_data.groupby(level='Month')['Total'].sum()
    max_registrations = monthly_counts.max()
    most_popular_months = monthly_counts[monthly_counts == max_registrations].index.tolist()

    print(f"Most popular month(s) for {breed} dogs: {' '.join(most_popular_months)}")


if __name__ == '__main__':
    main()
