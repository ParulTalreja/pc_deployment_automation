import requests
from bs4 import BeautifulSoup as bs
import wget
from pathlib import Path
URL = 'http://10.41.24.115:9000/scheduled_deployments/2022-10-17/634d535b57f2f38727ea1c7e/deployments/634d535b57f2f38727ea1c80/DEPLOY/'
FILETYPE = '.txt'

def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')


for link in get_soup(URL).find_all('a'):
    file_link = link.get('href')
    if FILETYPE in file_link:
        print(file_link)     # txt file to get download
        with open(link.text, 'wb') as file:
            response = requests.get(URL + file_link)
            print_link = (URL + file_link)
            print(print_link)    # path where text file is available
            filename = wget.download(URL + file_link)
            print(filename)       # downloaded text file
            print(Path.cwd())

