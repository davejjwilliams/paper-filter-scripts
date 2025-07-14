# Paper Scraping Scripts

This repository contains scripts used to fetch and process papers from the ICSE Research Track.

## Setup

To run the scripts, you need to install the required dependencies:

```shell
pip install -r requirements.txt
```

## Script 1: Researchr Scraper

This script fetches all the papers from the . It takes two args as inputs: the link to the technical track website and the year (used for the output filename).

Output is stored under [/results/researchr/](/results/researchr/).

The following commands are run to retrieve papers from the past 3 years:

```shell
python scraper.py https://conf.researchr.org/track/icse-2023/icse-2023-technical-track?#event-overview 2023
```

```shell
python scraper.py https://conf.researchr.org/track/icse-2024/icse-2024-research-track?#event-overview 2024
```

```shell
python scraper.py https://conf.researchr.org/track/icse-2025/icse-2025-research-track?#event-overview 2025
```

## Script 2: Processing BIB files from ACM Advanced Search

This script takes as input the path to a .bib file generated from exporting the results in of an ACM Advanced Search, and produces a CSV.

Output is stored under [/results/bib/](/results/bib/).

The following commands are run to generate the results:

```shell
python script.py data/all-keywords.bib output.csv
```