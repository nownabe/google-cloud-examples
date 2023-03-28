List BigQuery Public Tables
===========================

## Usage

```bash
poetry install
poetry run python main.py
```

Help:

```bash
$ poetry run python main.py --help 
usage: main.py [-h] [--sort_by {rows,bytes}] [--project PROJECT] [--top_n TOP_N] [--dataset DATASET]

options:
  -h, --help            show this help message and exit
  --sort_by {rows,bytes}
  --project PROJECT     Project to run APIs
  --top_n TOP_N
  --dataset DATASET
```

## Result

```
bigquery-public-data:pypi.simple_requests                                1,237,030,461,049 rows
bigquery-public-data:pypi.file_downloads                                   516,656,363,573 rows
bigquery-public-data:deps_dev_v1.DependencyGraphEdges                      385,472,749,807 rows
bigquery-public-data:deps_dev_v1.Dependencies                              162,146,224,872 rows
bigquery-public-data:modis_terra_net_primary_production.MODIS_MOD17A3HGF    77,458,380,111 rows
bigquery-public-data:google_books_ngrams_2020.eng_5                         65,312,254,011 rows
bigquery-public-data:google_patents_research.annotations                    59,089,580,018 rows
bigquery-public-data:google_patents_research.annotations_202204             57,516,555,259 rows
bigquery-public-data:wikipedia.pageviews_2019                               57,010,621,048 rows
bigquery-public-data:wikipedia.pageviews_2020                               55,917,037,333 rows
bigquery-public-data:wikipedia.pageviews_2018                               55,571,590,705 rows
bigquery-public-data:google_patents_research.annotations_202111             54,518,187,461 rows
bigquery-public-data:wikipedia.pageviews_2017                               54,489,222,992 rows
bigquery-public-data:wikipedia.pageviews_2016                               53,314,598,093 rows
bigquery-public-data:wikipedia.pageviews_2021                               53,288,623,350 rows
bigquery-public-data:google_patents_research.annotations_202105             53,050,364,781 rows
bigquery-public-data:wikipedia.pageviews_2022                               52,686,252,969 rows
bigquery-public-data:google_patents_research.annotations_202101             51,928,230,588 rows
bigquery-public-data:google_patents_research.annotations_202007             47,676,364,297 rows
bigquery-public-data:wise_all_sky_data_release.mep_wise                     42,820,194,581 rows
bigquery-public-data:google_books_ngrams_2020.eng_us_5                      39,615,448,791 rows
bigquery-public-data:wikipedia.pageviews_2015                               36,868,931,374 rows
bigquery-public-data:google_books_ngrams_2020.eng_3                         23,137,262,595 rows
bigquery-public-data:google_books_ngrams_2020.eng_4                         22,420,996,755 rows
bigquery-public-data:crypto_polygon.traces                                  21,061,261,027 rows
bigquery-public-data:google_books_ngrams_2020.eng_us_3                      14,851,423,689 rows
bigquery-public-data:google_books_ngrams_2020.eng_us_4                      13,992,520,329 rows
bigquery-public-data:google_books_ngrams_2020.eng_bert_preprocessed         13,182,520,884 rows
bigquery-public-data:google_books_ngrams_2020.eng_gb_5                      13,151,465,219 rows
bigquery-public-data:google_books_ngrams_2020.fre_5                         13,113,597,224 rows
```
