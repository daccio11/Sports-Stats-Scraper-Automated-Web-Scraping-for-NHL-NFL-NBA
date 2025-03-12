from NHL_scraping import scrape_nhl_stats  # Import NHL scraper
from NBA_scraping import scrape_nba_stats  # Import NBA scraper
from NFL_scraping import scrape_nfl_stats  # Import NHL scraper

def get_dataset_choice(options):
    # Asks the user to choose which dataset they want to download.
    #
    # Parameters:
    #     options (dict): A dictionary where keys are dataset numbers (as strings)
    #                     and values are tuples containing dataset names and their scraping functions.
    #
    # Returns:
    #     str: The selected dataset key or 'exit' if the user chooses to exit.

    while True:
        print("\nWhich dataset would you like to download?")

        # Display dataset options
        for key, (name, scrap) in options.items():
            print(f"{key}. {name}")  # Show available datasets

        print("0. Exit")  # Add an exit option

        choice = input("Enter the number corresponding to your choice: ")

        if choice == "0":
            print("👋 Exiting program. Goodbye!")
            return "exit"  # Return 'exit' to indicate user wants to quit
        elif choice in options:
            return choice  # Return the selected dataset key
        else:
            print("❌ Invalid selection. Please enter a valid number.")


def get_download_choice(df, dataset_name):
    # Asks the user to choose the format for downloading the dataset and saves the file.
    #
    # Parameters:
    #     df (pd.DataFrame): The Pandas DataFrame containing the scraped data.
    #     dataset_name (str): The name of the dataset (used for file naming).
    #
    # Returns:
    #     None

    while True:
        print("\nHow would you like to download the data?")
        print("1. CSV (Excel Compatible)")
        print("2. Excel (.xlsx)")
        print("3. JSON")
        print("0. Cancel and Choose Another Dataset")  # Option to go back

        choice = input("Enter the number corresponding to your choice: ")

        filename = dataset_name.replace(" ", "_")  # Clean filename

        if choice == "1":
            df.to_csv(f"{filename}.csv", index=False)
            print(f"✅ Data saved as '{filename}.csv'")
            break
        elif choice == "2":
            df.to_excel(f"{filename}.xlsx", index=False)
            print(f"✅ Data saved as '{filename}.xlsx'")
            break
        elif choice == "3":
            df.to_json(f"{filename}.json", orient="records")
            print(f"✅ Data saved as '{filename}.json'")
            break
        elif choice == "0":
            print("🔄 Returning to dataset selection...")
            return  # Go back to dataset selection
        else:
            print("❌ Invalid choice. Please select a valid format.")


# Main Loop to Keep Asking for Dataset
def main():
    # Main function that allows the user to choose and download datasets repeatedly until they choose to exit.

    datasets = {
        "1": ("NHL Statistical Leaders", scrape_nhl_stats),
        "2": ("NFL Rushing Leaders", scrape_nfl_stats),
        "3": ("NBA Scoring Leaders", scrape_nba_stats)
    }

    while True:
        dataset_choice = get_dataset_choice(datasets)  # Ask user to pick a dataset

        if dataset_choice == "exit":
            break  # Exit the loop if user chooses to quit

        dataset_name, scrape_function = datasets[dataset_choice]  # Get dataset details
        df = scrape_function()  # Call the scraping function

        if df is not None:
            get_download_choice(df, dataset_name)  # Ask how to download the dataset
        else:
            print("❌ Failed to retrieve dataset. Try again.")

    print("🎉 Program finished. Thanks for using the scraper!")


# Run the main function
if __name__ == "__main__":
    main()
