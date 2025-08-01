# Paper Scraping Scripts

This repository contains scripts used to fetch and process papers from the ICSE Research Track.

## TODO

- Reviewers to add `True` or `False` to the `relevant` column for the papers assigned to them in [`AI_ICSE2023_papers.csv`](AI_ICSE2023_papers.csv) and [`AI_ICSE2024_papers.csv`](AI_ICSE2024_papers.csv).

## Setup

To run the scripts, you need to install the required dependencies:

```shell
pip install -r requirements.txt
```

## [`scraper.py`](scraper.py): Researchr Website Scraper

This script fetches all the papers from the Researchr conference websites. It takes two args as inputs: the link to the technical track website and the year (used for the output filename).

Output is stored under [`/results/researchr/`](/results/researchr/).

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

## [`bib-converter.py`](bib-converter.py): Processing BIB files from ACM Advanced Search

This script has two modes of use:

1. Takes as input the path to a .bib file generated from exporting the results in of an ACM Advanced Search, and produces a CSV with columns Title, Authors, URL and Abstract.

Examples:

```shell
python bib-converter.py data/2023/2023ICSE.bib 2023_papers.csv
```

```shell
python bib-converter.py data/2024/2024ICSE.bib 2024_papers.csv
```

1. If the `icse` param is provided, this will search the relevant directory (e.g. [`/data/2023/`](/data/2023/) for 2023) and retrieve the expected files ([`2023ICSE_Artifact_Available.bib`](/data/2023/2023ICSE_Artifact_Available.bib), [`2023ICSE_Artifact_Reusable.bib`](/data/2023/2023ICSE_Artifact_Reusable.bib), [`2023ICSE_Artifact_Functional.bib`](/data/2023/2023ICSE_Artifact_Functional.bib), and [`2023ICSE_AI.bib`](/data/2023/2023ICSE_AI.bib)) to check which papers have artifacts and to what extent they are replicable. Finally, it produces a CSV with columns Title, Authors, URL, Abstract, Artifacts Available (Bool), Artifacts Reusable (Bool), Artifacts Functional (Bool), and AI (Bool).

The following commands are run to generate the results:

Examples:

```shell
python bib-converter.py --icse 2023 ICSE2023_papers.csv
```

```shell
python bib-converter.py --icse 2024 ICSE2024_papers.csv
```

All outputs are stored in [`/results/bib/`](/results/bib/).

## [`assign_reviewers.py`](assign_reviewers.py): Assigning Reviewers to Review Papers for Relevancy

This script takes as input either [`/results/bib/ICSE2023_papers.csv`](/results/bib/ICSE2023_papers.csv) or [`/results/bib/ICSE2024_papers.csv`](/results/bib/ICSE2024_papers.csv). The second input is the output csv file name. The third and final output is a comma-separated list of reviewer initials. The script selects the papers marked as AI from the input CSV file and evenly assigns reviewers.

Examples:

```shell
python assign_reviewers.py results/bib/ICSE2023_papers.csv AI_ICSE2023_papers.csv DW,AA,JP,FS
```

```shell
python assign_reviewers.py results/bib/ICSE2024_papers.csv AI_ICSE2024_papers.csv DW,AA,JP,FS
```

Output files are:

- [`AI_ICSE2023_papers.csv`](AI_ICSE2023_papers.csv)
- [`AI_ICSE2024_papers.csv`](AI_ICSE2024_papers.csv)

## Analysis

Basic analysis of the papers for ICSE 2023/2024 is provided in [`analysis.ipynb`](analysis.ipynb).