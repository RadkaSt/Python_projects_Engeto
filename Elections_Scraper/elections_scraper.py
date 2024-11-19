"""

elections_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Radka Štorchová

email: r.storchova@gmail.com

discord: radkastorchova

"""
import csv
import requests
import sys
from bs4 import BeautifulSoup


def main():
    """
    Main function to coordinate the entire process:
    - Validate input arguments
    - Scrape data from a given URL
    - Save results to a CSV file
    """
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    validate_inputs(base_url)
    url = sys.argv[1]
    file_name = sys.argv[2]
    initial_soup = fetch_html(url)
    data_rows, csv_header = process_municipality_data(initial_soup, base_url)
    print(f"Saving data to file: {file_name}")
    write_to_csv(data_rows, csv_header, file_name)
    print("Data successfully saved. Process completed.")


def validate_inputs(base_url):
    """
    Validate command-line arguments to ensure they are correct.
    Exits the program if arguments are invalid.
    """
    if len(sys.argv) != 3:
        print("Incorrect number of arguments. Refer to the README and try again.")
        exit()
    elif base_url not in sys.argv[1]:
        print("Invalid URL provided. Refer to the README for correct usage.")
        exit()
    elif ".csv" not in sys.argv[2]:
        print("Invalid file name provided. Ensure it ends with '.csv'.")
        exit()
    else:
        print(f"Fetching data from the URL: {sys.argv[1]}")


def fetch_html(url):
    """
    Fetch the HTML content of the given URL and return a BeautifulSoup object.
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def process_municipality_data(initial_soup, base_url):
    """
    Extract links to municipality data and process them to collect relevant information.
    - Returns a list of rows (data) and a header (column names) for the CSV.
    """
    data_rows = []
    csv_header = []
    region_index = 0  # Track which region is being processed

    # Find all municipality names
    names = initial_soup.find_all('td', {'class': 'overflow_name'})

    # Loop through all municipality rows
    for municipality in initial_soup.find_all('td', {'class': 'cislo'}):
        row = [municipality.text]  # Start row with the municipality code
        row.append(names[region_index].text)  # Add municipality name

        # Get link to detailed results
        link = municipality.a['href']
        detailed_soup = fetch_html(base_url + link)

        # If processing the first region, create the header
        if region_index == 0:
            csv_header = generate_csv_header(detailed_soup)

        # Collect data for the current municipality and append to the row
        row.extend(extract_election_data(detailed_soup))
        data_rows.append(row)
        region_index += 1

    return data_rows, csv_header


def generate_csv_header(soup):
    """
    Generate the header (column names) for the CSV file based on the data structure.
    """
    header = ["Code", "Location", "Registered", "Envelopes", "Valid"]
    for party in soup.find_all('td', {'class': 'overflow_name'}):
        header.append(party.text)
    return header


def extract_election_data(soup):
    """
    Extract numerical data such as registered voters, envelopes, and votes.
    - Returns a list of data values for a single municipality.
    """
    data = []

    # Collect data for registered voters, envelopes, and valid votes
    registered = soup.find('td', {'headers': 'sa2'}).text
    data.append(clean_text(registered))
    envelopes = soup.find('td', {'headers': 'sa5'}).text
    data.append(clean_text(envelopes))
    valid = soup.find('td', {'headers': 'sa6'}).text
    data.append(clean_text(valid))

    # Collect vote counts for each party
    data.extend(collect_vote_counts(soup))

    return data


def collect_vote_counts(soup):
    """
    Collect the number of votes for each political party from the detailed results page.
    - Returns a list of vote counts.
    """
    votes = []
    table_index = 1
    total_tables = len(soup.find_all('table'))

    # Loop through vote tables and extract data
    while table_index < total_tables:
        vote_data = soup.find_all('td', {'headers': f't{table_index}sa2 t{table_index}sb3'})
        for vote in vote_data:
            votes.append(clean_text(vote.text))
        table_index += 1

    return votes


def clean_text(text):
    """
    Clean the input text by removing unwanted characters such as non-breaking spaces.
    """
    return ''.join(text.split()) if "\xa0" in text else text


def write_to_csv(data_rows, header, file_name):
    """
    Write the collected data into a CSV file.
    """
    with open(file_name, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, dialect="excel")
        writer.writerow(header)  # Write the header
        writer.writerows(data_rows)  # Write the data rows


if __name__ == "__main__":
    main()
