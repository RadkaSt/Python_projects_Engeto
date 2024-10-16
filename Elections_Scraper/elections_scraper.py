#importing libraries
import requests
from bs4 import BeautifulSoup
import csv
import sys
import re


def get_soup(url):
    """
    Stáhne webovou stránku a vytvoří objekt BeautifulSoup pro parsování HTML.

    :param url: URL adresa stránky ke stažení
    :return: Objekt BeautifulSoup
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def scrape_results(url):
    """
    Scrapuje výsledky voleb pro jednu obec.

    :param url: URL adresa stránky s výsledky pro obec
    :return: Seznam výsledků pro danou obec
    """
    soup = get_soup(url)
    results = []

    # Získání názvu obce
    obec_name = soup.find('h3').text.strip()

    # Nalezení všech tabulek na stránce
    tables = soup.find_all('table')

    # Získání dat o volební účasti
    turnout_data = tables[0].find_all('td')
    registered = turnout_data[3].text.strip()  # Počet registrovaných voličů
    envelopes = turnout_data[4].text.strip()  # Počet vydaných obálek
    valid_votes = turnout_data[7].text.strip()  # Počet platných hlasů

    # Scrapování výsledků pro jednotlivé strany
    for row in tables[1].find_all('tr')[2:]:  # Přeskočení prvních dvou řádků (záhlaví)
        cells = row.find_all('td')
        if len(cells) > 0:
            party = cells[1].text.strip()  # Název strany
            votes = cells[2].text.strip()  # Počet hlasů pro stranu
            results.append([obec_name, registered, envelopes, valid_votes, party, votes])

    return results


def scrape_district(url):
    """
    Scrapuje výsledky voleb pro celý okres.

    :param url: URL adresa stránky s přehledem obcí v okrese
    :return: Seznam výsledků pro všechny obce v okrese
    """
    soup = get_soup(url)
    all_results = []

    # Procházení všech řádků tabulky s obcemi
    for row in soup.find('table', {'class': 'table'}).find_all('tr')[2:]:
        cells = row.find_all('td')
        if len(cells) > 0:
            # Sestavení URL pro detail obce
            link = 'https://www.volby.cz/pls/ps2017nss/' + cells[0].find('a')['href']
            all_results.extend(scrape_results(link))

    return all_results


def is_valid_url(url):
    """
    Kontroluje, zda zadaná URL odpovídá očekávanému formátu pro stránky s volebními výsledky.

    :param url: URL adresa ke kontrole
    :return: True, pokud je URL platná, jinak False
    """
    pattern = r'^https://www\.volby\.cz/pls/ps2017nss/ps32\?xjazyk=CZ&xkraj=\d+&xnumnuts=\d+'
    return re.match(pattern, url) is not None


def main():
    """
    Hlavní funkce skriptu. Zpracovává argumenty příkazové řádky, 
    spouští scrapování a ukládá výsledky do CSV souboru.
    """
    # Kontrola počtu argumentů
    if len(sys.argv) != 3:
        print("Chyba: Prosím, zadejte dva argumenty - URL a název výstupního souboru.")
        print(
            "Příklad: python script.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 vysledky_prostejov.csv")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    # Kontrola platnosti URL
    if not is_valid_url(url):
        print("Chyba: Neplatná URL. Prosím, zadejte platnou URL pro územní celek.")
        sys.exit(1)

    # Kontrola přípony výstupního souboru
    if not output_file.endswith('.csv'):
        print("Chyba: Výstupní soubor musí mít příponu .csv")
        sys.exit(1)

    # Scrapování výsledků
    results = scrape_district(url)

    # Zápis výsledků do CSV souboru
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Obec', 'Registrovaní voliči', 'Vydané obálky', 'Platné hlasy', 'Strana', 'Počet hlasů'])
        writer.writerows(results)

    print(f"Výsledky byly úspěšně uloženy do souboru {output_file}")


if __name__ == '__main__':
    main()
