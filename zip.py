import os
import zipfile
from pathlib import Path
def zips():
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


if __name__ == "__main__":
    zips()
