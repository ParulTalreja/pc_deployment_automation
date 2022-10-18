import os
from pathlib import Path
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

if __name__ == "__main__":pwd

    tarfiles()
