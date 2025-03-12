import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML
import pandas as pd  # For handling data
from tabulate import tabulate  # For displaying DataFrame in table format


def scrape_nhl_stats():
# Scrapes NHL statistical leaders from Wikipedia and returns a Pandas DataFrame.

    url = "https://en.wikipedia.org/wiki/List_of_NHL_statistical_leaders"  # Wikipedia page URL

    # Send a GET request to fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML content

    # Check if the request was successful
    if response.status_code != 200:
        print("❌ Failed to fetch data from Wikipedia.")  # Print error message if request fails
        return None  # Return None to indicate failure

    # Locating the correct table
    table = soup.find_all('table')[2]

    # Extract column headers from the table
    headers = table.find_all("th")  # Find all table headers

    # Clean and store header titles
    table_headers = [title.text.strip() for title in headers[0:6]]  # Extract first 6 headers because the ranks in the rows are listed as "th"
    #print(rank_table_titles)  # Debugging output

    # Initialize an empty DataFrame with extracted column names
    df = pd.DataFrame(columns=table_headers)

    # Extract all rows from the table
    collumn_data = table.find_all('tr')

    # Iterate through each row (excluding the header row)
    for row in collumn_data[1:]:
        th = row.find('th')  # Extract the first column (Rank) if available
        row_data = row.find_all('td')  # Extract all other columns (player stats)

        # If `th` exists, add its text to the row data; otherwise, start with an empty list
        indv_row_data = [th.text.strip()] if th else []
        # Extract text from all <td> elements and append to the row data
        indv_row_data += [data.text.strip() for data in row_data]

        #print(indv_row_data)  # Debugging output

        length = len(df)  # Get current DataFrame length to determine next row index
        df.loc[length] = indv_row_data  # Append new row to the DataFrame

    return df  # Return the final DataFrame containing the scraped data


# Uncomment the following line to display the table in a formatted style in IDE
# print(tabulate(df, headers='keys', tablefmt='psql'))

