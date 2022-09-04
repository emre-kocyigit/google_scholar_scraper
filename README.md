# google_scholar_scraper
This project provides organised form of Google Scholar papers according to keywords and page number.

## required packages
These packages should be installed:
- requests
- re
- pandas
- time
- bs4

## inputs
There are only two parameters for now. 
1. keywords --> should be a string as below example:
      - Ex1: keywords = "dark+patterns"
      - Ex2: keywords = "phishing+detection+with+machine+learning"
2. page number --> should be integer value
      - Ex:  page_number = 2

## output
Output is an organized csv file which contains following headers and their information, which is scraped from the Google Scholar, according to your inputs:
- Title
- Year
- Author
- Citation
- Publication
- Link

I added an example output file as "dark_pattern_papers.csv".
## important notes
- There are 10 papers on each page of Google Scholar. If you want to see 100 papers, your page number input value should be 10.
- Before you run the file, be sure about the total page number on your browser. Page number value should be less or equal than total page number.
- This python file was created in a day and not tested well. So, don't be suprised if you face any bug :)
- Author section contains only one author. If you want to cite a paper from the csv file, do not forget to check all authors of the paper!
