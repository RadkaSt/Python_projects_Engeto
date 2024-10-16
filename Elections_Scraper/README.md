# Elections results scraper
Tento Python skript scrapuje výsledky voleb z webové stránky [volby.cz](https://www.volby.cz/) a ukládá je do CSV souboru. Skript zpracovává volební výsledky pro jednotlivé obce v zadaném okrese.

## Funkce

- Stahuje volební výsledky z webu volby.cz pro zadaný územní celek.
- Scrapuje informace o účasti voličů (registrovaní voliči, vydané obálky, platné hlasy).
- Scrapuje výsledky pro jednotlivé politické strany v obci.
- Ukládá všechny výsledky do CSV souboru.

## Požadavky

Před spuštěním skriptu je nutné nainstalovat potřebné knihovny. Vytvořte si prostředí a nainstalujte knihovny uvedené v `requirements.txt`:

```
pip install -r requirements.txt
```

### Knihovny

- `requests` - Stahování obsahu webových stránek.
- `beautifulsoup4` - Parsování HTML stránek.
- `lxml` - Rychlý XML/HTML parser.

## Instalace

1. Naklonujte si tento repozitář nebo si stáhněte soubory.
2. Ujistěte se, že máte nainstalovaný Python (minimálně verze 3.6).
3. Nainstalujte požadované balíčky pomocí příkazu:

   ```
   pip install -r requirements.txt
   ```

## Použití

Skript přijímá dva argumenty z příkazové řádky:

1. **URL volebního okrsku** - URL na stránku, která obsahuje seznam obcí pro daný okres (např. [Odkaz na Prostějov](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103)).
2. **Název CSV souboru** - Cesta k souboru, do kterého budou výsledky uloženy (musí mít příponu `.csv`).

### Příklad použití

```
python elections_scraper.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 vysledky_prostejov.csv
```

Tento příkaz stáhne výsledky voleb pro okres Prostějov a uloží je do souboru `vysledky_prostejov.csv`.

### Struktura CSV souboru

Výstupní CSV soubor bude obsahovat následující sloupce:

- **Obec** - Název obce
- **Registrovaní voliči** - Počet registrovaných voličů v obci
- **Vydané obálky** - Počet vydaných obálek
- **Platné hlasy** - Počet platných hlasů
- **Strana** - Název politické strany
- **Počet hlasů** - Počet hlasů pro danou stranu

### Ukázkový výstup

| Obec     | Registrovaní voliči | Vydané obálky | Platné hlasy | Strana            | Počet hlasů |
|----------|---------------------|---------------|--------------|-------------------|-------------|
| Prostějov| 20,000               | 15,000        | 14,500       | Strana A          | 5,000       |
| Prostějov| 20,000               | 15,000        | 14,500       | Strana B          | 4,500       |
| Prostějov| 20,000               | 15,000        | 14,500       | Strana C          | 3,000       |

## Omezení

- Tento skript je specificky napsán pro volební výsledky z roku 2017 (PS2017) a může být nutné jej přizpůsobit pro jiné typy voleb.
- Skript očekává specifickou strukturu HTML stránek na volby.cz a může selhat, pokud se struktura stránky změní.
