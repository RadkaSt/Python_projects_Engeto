# Elections results scraper
This program scrapes election data from the Czech election website and saves it into a CSV

## Features

- Scrapes election data from a given municipality URL.
- Collects data such as registered voters, envelopes, valid votes, and votes for individual parties.
- Outputs the data into a neatly formatted CSV file.

---
## Prerequisites

Before you run the program, ensure you have the following installed:

1. **Python 3.7 or higher**
2. Required Python libraries:
   - `beautifulsoup4`
   - `requests`

You can install the dependencies using `pip`:

```bash
pip install beautifulsoup4 requests
or
```
pip install -r requirements.txt
```

## Usage
The program is run from the command line and requires two arguments:

    URL: A link to the election data page on the Czech election website.
    Output File: The name of the CSV file where the data will be saved.
```
python election_scraper.py <URL> <output_file.csv>
```

### Usage example

```
python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"

```

### Notes

    The URL must belong to the domain https://www.volby.cz/pls/ps2017nss/.
    The output file must have a .csv extension.

## Output

The program creates a CSV file containing election data with the following structure:
Code	Location	Registered	Envelopes	Valid	Party 1	Party 2	...

    Code: Municipality code.
    Location: Municipality name.
    Registered: Number of registered voters.
    Envelopes: Number of envelopes submitted.
    Valid: Number of valid votes.
    Party N: Votes for each political party.
