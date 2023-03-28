# List BigQuery Public Tables

## Usage

```bash
go run .
```

Options:

```bash
$ go run .
Usage of /tmp/go-build2399083553/b001/exe/list-bigquery-public-tables:
  -dataset string
        if this is set, tables in the specified dataset will be listed
  -project string
        project to run APIs
  -sortby string
        sort tables by bytes or number of rows (default "rows")
  -topn int
        Number of top tables to list (default 30)
```

## Results

Top 30 tables with the most rows:

```
bigquery-public-data:pypi.simple_requests                                 1,237,184,240,444 rows 265,567,130,144,227 bytes
bigquery-public-data:pypi.file_downloads                                    516,719,004,334 rows 197,356,041,202,729 bytes
bigquery-public-data:deps_dev_v1.DependencyGraphEdges                       385,472,749,807 rows  52,116,130,663,202 bytes
bigquery-public-data:deps_dev_v1.Dependencies                               162,146,224,872 rows  14,070,340,610,514 bytes
bigquery-public-data:modis_terra_net_primary_production.MODIS_MOD17A3HGF     77,458,380,111 rows  15,491,676,022,200 bytes
bigquery-public-data:google_books_ngrams_2020.eng_5                          65,312,254,011 rows  81,194,225,835,991 bytes
bigquery-public-data:google_patents_research.annotations                     59,089,580,018 rows   6,625,316,692,228 bytes
bigquery-public-data:google_patents_research.annotations_202204              57,516,555,259 rows   6,451,932,750,331 bytes
bigquery-public-data:wikipedia.pageviews_2019                                57,010,621,048 rows   2,541,009,499,603 bytes
bigquery-public-data:wikipedia.pageviews_2020                                55,917,037,333 rows   2,478,394,175,001 bytes
bigquery-public-data:wikipedia.pageviews_2018                                55,571,590,705 rows   2,471,947,508,849 bytes
bigquery-public-data:google_patents_research.annotations_202111              54,518,187,461 rows   6,074,696,085,164 bytes
bigquery-public-data:wikipedia.pageviews_2017                                54,489,222,992 rows   2,415,465,800,641 bytes
bigquery-public-data:wikipedia.pageviews_2016                                53,314,598,093 rows   2,351,945,393,381 bytes
bigquery-public-data:wikipedia.pageviews_2021                                53,288,623,350 rows   2,361,648,780,422 bytes
bigquery-public-data:google_patents_research.annotations_202105              53,050,364,781 rows   5,951,030,313,000 bytes
bigquery-public-data:wikipedia.pageviews_2022                                52,686,252,969 rows   2,345,934,514,732 bytes
bigquery-public-data:google_patents_research.annotations_202101              51,928,230,588 rows   5,731,369,666,253 bytes
bigquery-public-data:google_patents_research.annotations_202007              47,676,364,297 rows   5,256,116,693,488 bytes
bigquery-public-data:wise_all_sky_data_release.mep_wise                      42,820,194,581 rows  15,954,709,607,201 bytes
bigquery-public-data:google_books_ngrams_2020.eng_us_5                       39,615,448,791 rows  48,615,818,459,279 bytes
bigquery-public-data:wikipedia.pageviews_2015                                36,868,931,374 rows   1,646,400,144,144 bytes
bigquery-public-data:google_books_ngrams_2020.eng_3                          23,137,262,595 rows  31,330,608,616,025 bytes
bigquery-public-data:google_books_ngrams_2020.eng_4                          22,420,996,755 rows  29,040,175,977,222 bytes
bigquery-public-data:crypto_polygon.traces                                   21,061,261,027 rows  14,110,665,216,716 bytes
bigquery-public-data:google_books_ngrams_2020.eng_us_3                       14,851,423,689 rows  19,802,662,423,981 bytes
bigquery-public-data:google_books_ngrams_2020.eng_us_4                       13,992,520,329 rows  17,876,485,696,976 bytes
bigquery-public-data:google_books_ngrams_2020.eng_bert_preprocessed          13,182,520,884 rows     681,535,039,226 bytes
bigquery-public-data:google_books_ngrams_2020.eng_gb_5                       13,151,465,219 rows  18,128,339,771,017 bytes
bigquery-public-data:google_books_ngrams_2020.fre_5                          13,113,597,224 rows  17,981,427,376,286 bytes

```

Top 30 tables with the largest data size:

```
bigquery-public-data:pypi.simple_requests                                          1,237,198,150,816 rows 265,570,174,552,195 bytes
bigquery-public-data:pypi.file_downloads                                             516,725,031,707 rows 197,358,419,844,845 bytes
bigquery-public-data:noaa_global_forecast_system.NOAA_GFS0P25                         10,131,947,672 rows 172,575,901,901,656 bytes
bigquery-public-data:google_books_ngrams_2020.eng_5                                   65,312,254,011 rows  81,194,225,835,991 bytes
bigquery-public-data:deps_dev_v1.DependencyGraphEdges                                385,472,749,807 rows  52,116,130,663,202 bytes
bigquery-public-data:google_books_ngrams_2020.eng_us_5                                39,615,448,791 rows  48,615,818,459,279 bytes
bigquery-public-data:google_books_ngrams_2020.eng_3                                   23,137,262,595 rows  31,330,608,616,025 bytes
bigquery-public-data:google_books_ngrams_2020.eng_4                                   22,420,996,755 rows  29,040,175,977,222 bytes
bigquery-public-data:google_books_ngrams_2020.eng_us_3                                14,851,423,689 rows  19,802,662,423,981 bytes
bigquery-public-data:google_books_ngrams_2020.eng_gb_5                                13,151,465,219 rows  18,128,339,771,017 bytes
bigquery-public-data:google_books_ngrams_2020.fre_5                                   13,113,597,224 rows  17,981,427,376,286 bytes
bigquery-public-data:google_books_ngrams_2020.eng_us_4                                13,992,520,329 rows  17,876,485,696,976 bytes
bigquery-public-data:wise_all_sky_data_release.mep_wise                               42,820,194,581 rows  15,954,709,607,201 bytes
bigquery-public-data:modis_terra_net_primary_production.MODIS_MOD17A3HGF              77,458,380,111 rows  15,491,676,022,200 bytes
bigquery-public-data:google_books_ngrams_2020.ger_5                                   11,162,274,931 rows  14,628,620,977,237 bytes
bigquery-public-data:crypto_polygon.traces                                            21,061,261,027 rows  14,110,665,216,716 bytes
bigquery-public-data:deps_dev_v1.Dependencies                                        162,146,224,872 rows  14,070,340,610,514 bytes
bigquery-public-data:google_books_ngrams_2020.ger_3                                    6,753,507,494 rows   9,415,055,210,066 bytes
bigquery-public-data:google_books_ngrams_2020.spa_5                                    6,397,984,484 rows   8,637,482,624,682 bytes
bigquery-public-data:google_books_ngrams_2020.eng_gb_3                                 5,448,485,120 rows   8,289,090,411,346 bytes
bigquery-public-data:google_books_ngrams_2020.fre_3                                    5,112,201,755 rows   8,061,871,411,655 bytes
bigquery-public-data:google_books_ngrams_2020.eng_gb_4                                 4,900,769,271 rows   7,101,286,209,704 bytes
bigquery-public-data:google_books_ngrams_2020.eng_fiction_5                            6,167,549,750 rows   6,925,776,623,092 bytes
bigquery-public-data:google_books_ngrams_2020.fre_4                                    4,713,076,504 rows   6,916,502,962,768 bytes
bigquery-public-data:google_books_ngrams_2020.ger_4                                    4,948,393,741 rows   6,710,352,243,612 bytes
bigquery-public-data:google_patents_research.annotations                              59,089,580,018 rows   6,625,316,692,228 bytes
bigquery-public-data:google_patents_research.annotations_202204                       57,516,555,259 rows   6,451,932,750,331 bytes
bigquery-public-data:google_patents_research.annotations_202111                       54,518,187,461 rows   6,074,696,085,164 bytes
bigquery-public-data:google_patents_research.annotations_202105                       53,050,364,781 rows   5,951,030,313,000 bytes
bigquery-public-data:human_genome_variants.1000_genomes_phase_3_variants_20150220         84,801,880 rows   5,909,919,588,657 bytes
```
