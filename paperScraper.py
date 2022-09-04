# import necessary packages. Install them, if they are not installed!
import requests
import re
import pandas as pd
import time
from bs4 import BeautifulSoup

# these are necessary because google scholar webpage requires login
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

# parameters
keywords = "dark+patterns"
page_number = 2


# Functions
# this function for getting the information of the web page and parse it
def get_paper_info(url):
    response = requests.get(url, headers=headers)  # download the webpage

    if response.status_code != 200:  # check if response is successful
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ')

    paper_doc = BeautifulSoup(response.text, 'html.parser')  # parse html file by BeautifulSoup module

    return paper_doc


# this function for extracting tags of 'paper', 'cite', 'link' and 'author'
def get_tags(doc):
    paper_tag = doc.select('[data-lid]')
    cite_divs = doc.find_all('div', {"class": "gs_ri"})
    cite_tag = []
    for index in range(0,10):  # there is a 10 publications on each page, so be careful about the '10'
        check = cite_divs[index].next_element.nextSibling.next_sibling.next_sibling.text
        if 'Cited by' in check:
            cite_tag.append(check)
        else:
            cite_tag.append(0)
    link_tag = doc.find_all('h3', {"class": "gs_rt"})
    author_tag = doc.find_all("div", {"class": "gs_a"})

    return paper_tag, cite_tag, link_tag, author_tag


# this will return the title of the paper
def get_paper_title(paper_tag):
    paper_titles = []
    for tag in paper_tag:
        paper_titles.append(tag.select('h3')[0].get_text())

    return paper_titles


# this will return the citation number of the paper
def get_cite_count(cite_tag):
    cite_count = []
    for text in cite_tag:
        if text is None or text == 0:  # if paper has no citation then consider 0
            cite_count.append(int(0))
        else:
            tmp = re.search(r'\d+', text)  # re for removing the string " cited by "
            # and return only integer value
            if tmp is None:
                cite_count.append(0)
            else:
                cite_count.append(int(tmp.group()))

    return cite_count


# this will return link information
def get_link(link_tag):
    links = []
    for i in range(len(link_tag)):
        links.append(link_tag[i].a['href'])
    return links


# this function for getting authors, year and publication information
def get_details(authors_tag):
    years = []
    publication = []
    authors = []
    for i in range(len(authors_tag)):
        authortag_text = authors_tag[i].text.split()
        year = int(re.search(r'\d{4}', authors_tag[i].text).group())
        years.append(year)
        publication.append(authortag_text[-1])
        author = authortag_text[0] + ' ' + re.sub(',', '', authortag_text[1])
        authors.append(author)

    return years, publication, authors


# creating final repository
paper_repos_dict = {
                    'Title': [],
                    'Year': [],
                    'Author': [],
                    'Citation': [],
                    'Publication': [],
                    'Link': []}


# to create a dataframe according to the repository
def add_in_paper_repo(paper_name, year, author, cite, publication, link):
    paper_repos_dict['Title'].extend(paper_name)
    paper_repos_dict['Year'].extend(year)
    paper_repos_dict['Author'].extend(author)
    paper_repos_dict['Citation'].extend(cite)
    paper_repos_dict['Publication'].extend(publication)
    paper_repos_dict['Link'].extend(link)

    return pd.DataFrame(paper_repos_dict)



limit = page_number * 10  # because start=00 --> page 1, 10 --> page 2 ...  in google scholar
for i in range(0, limit, 10):
    print(i, ". turn")
    # get url for each page
    url = "https://scholar.google.com/scholar?start={}&q={}+&hl=en&as_sdt=0,5".format(i, keywords)

    # get content of the selected page
    doc = get_paper_info(url)

    # collect the tags
    paper_tag, cite_tag, link_tag, author_tag = get_tags(doc)

    # title of paper
    paper_title = get_paper_title(paper_tag)

    # year , author , publication of paper
    year, publication, author = get_details(author_tag)

    # cite number of paper
    cite = get_cite_count(cite_tag)

    # url of paper
    link = get_link(link_tag)

    # add in paper repo dict
    final = add_in_paper_repo(paper_title, year, author, cite, publication, link)

    # use sleep to avoid status code 429
    time.sleep(30)


final.to_csv("dark_pattern_papers.csv", sep=";", index=False, header=True)
