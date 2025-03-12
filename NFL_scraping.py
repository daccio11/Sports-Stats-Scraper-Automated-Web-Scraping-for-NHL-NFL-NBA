import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML
import pandas as pd  # For handling  data
from tabulate import tabulate  # For displaying DataFrame in a formatted table


def scrape_nfl_stats():
# Scrapes NFL career rushing yards leaders from Wikipedia and returns a Pandas DataFrame.

    url = "https://en.wikipedia.org/wiki/List_of_NFL_career_rushing_yards_leaders"  # Wikipedia page URL

    # Send a GET request to fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML content

    # Check if the request was successful
    if response.status_code != 200:
        print("❌ Failed to fetch data from Wikipedia.")  # Print error message if request fails
        return None  # Return None to indicate failure

    # Locate the correct table
    table = soup.find_all('table')[1]

    # Extract all column headers from the table
    headers = table.find_all("th")  # Find all <th> elements (column headers)

    # Clean and store header titles
    table_headers = [title.text.strip() for title in headers] # Strip spaces and newlines

    # print(rank_table_titles)  # Debugging: Print extracted column headers
    columns = table_headers  # Assign column names

    # Initialize an empty DataFrame with extracted column names
    df = pd.DataFrame(columns=table_headers)

    # Find the table body that contains all player data
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')  # Get all rows inside <tbody>

    # Iterate through each row (excluding the header row)
    for data in rows[1:]:  # Skip the header row
        row_data = data.find_all('td')  # Extract all <td> elements (table data)

        if not row_data:
            continue  # Skip empty rows

        # Extract text from each <td> element and strip unnecessary whitespace
        indv_row_data = [data.text.strip() for data in row_data]

        # print(indv_row_data)  # Debugging output to check extracted row data

        length = len(df)  # Get the current DataFrame length to determine the next row index
        df.loc[length] = indv_row_data  # Append new row to the DataFrame

    return df  # Return the final DataFrame containing the scraped data

# Uncomment the following line to display the table in a formatted style
# print(tabulate(df, headers='keys', tablefmt='psql'))
