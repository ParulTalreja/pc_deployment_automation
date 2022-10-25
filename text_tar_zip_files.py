import os
from pathlib import Path
from bs4 import BeautifulSoup as bs
import wget
import requests
import zipfile
URL = 'http://10.41.24.115:9000/scheduled_deployments/2022-10-17/634d535b57f2f38727ea1c7e/deployments/634d535b57f2f38727ea1c80/DEPLOY/'
FILETYPE = '.txt'

def tarfiles():
    
    file_name1 = "http://10.41.24.115:9000/scheduled_deployments/2022-10-06/633ea65073101ab294a986ef/deployments/633ea65073101ab294a986f1/entity_logs/retry_0/auto_pc_633ea65073101ab294a986f10/"
    os.system("wget -nH --cut-dirs=4 --recursive --no-parent -nv {0}".format(file_name1))
    print(Path.cwd())
    DIRS = '/Users/naveenkumar/PycharmProjects/pythonProject2'
    Tarfiles = []
    for root, dirs, files in os.walk(DIRS):
        for file in files:
            if file.endswith('.tar.gz'):
                path = os.path.join(root, file)
                if path.endswith('tar.gz'):
                    Tarfiles.append(path)
                    for i in Tarfiles:
                        os.system('tar -xvzf' + i + ' -C ~/Downloads/nav/')


def textfiles():
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


def zipfiles():
    file_name1 = "http://10.41.24.115:9000/scheduled_deployments/2022-10-06/633ea65073101ab294a986ef/deployments/633ea65073101ab294a986f1/entity_logs/retry_0/auto_pc_633ea65073101ab294a986f10/"
    os.system("wget -nH --cut-dirs=4 --recursive --no-parent -nv {0}".format(file_name1))
    print(Path.cwd())
    for root, dirs, files in os.walk('/Users/naveenkumar/PycharmProjects/pythonProject2'):
        for file in files:
            if file.endswith('.zip'):
                print(os.path.join(root, file))
                with zipfile.ZipFile(os.path.join(root, file), "r") as zip_ref:
                    zip_ref.extractall()
                    zip_ref.printdir()

if __name__ == "__main__":pwd

    tarfiles()
    textfiles()
    zipfiles()
