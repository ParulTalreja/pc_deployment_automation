import os
import pwd
import re
import subprocess
import zipfile

import requests


def tar_download_and_extract(PC_LOG_URL):
    file_name = 'home_nutanix_data_logs.tar.gz'
    file_url=PC_LOG_URL+file_name
    extract_folder = "resources"
    # Create the extraction folder if it doesn't exist
    os.makedirs(extract_folder, exist_ok=True)
    # Download the file
    response = requests.get(file_url)
    if response.status_code == 200:
        # Save the downloaded file locally
        downloaded_file_path = os.path.join(extract_folder, file_name)
        with open(downloaded_file_path, "wb") as f:
            f.write(response.content)
        print("File downloaded successfully.")
        tar_file_path="resources/home_nutanix_data_logs.tar.gz"

        # Run the tar command to extract the file
        command = ["tar", "-xvf", tar_file_path, "-C", extract_folder]
        extract_folder_url = "resources/home/nutanix/data/logs"
        try:
            subprocess.run(command, check=True)
            print("Extraction completed successfully.")
            os.remove(tar_file_path)
            return extract_folder_url
        except subprocess.CalledProcessError as e:
            print(f"Extraction failed: {e}")
    else:
        print("Failed to download the tar file. Please check if logs are available")

def zip_download_and_extract(PE_LOG_URL):
    # PE_LOG_URL:URL of the .zip file to download
    # Folder where you want to extract the contents
    extract_folder = "resources"

    # Create the extraction folder if it doesn't exist
    os.makedirs(extract_folder, exist_ok=True)

    zip_links=fetch_page_content(PE_LOG_URL)
    if not zip_links:
        print("No Zip file available at url ",PE_LOG_URL)
        return
    for zip_link in zip_links:
        file_url = PE_LOG_URL+zip_link
        download_and_save_zip_file(file_url,extract_folder,zip_link)
        os.remove(extract_folder+"/"+zip_link)




def download_and_save_zip_file(file_url,extract_folder,file_name):

    # URL containing links to the .zip files
    # Download the file
    response = requests.get(file_url)
    if response.status_code == 200:
        # Save the downloaded file locally
        downloaded_file_path = os.path.join(extract_folder,
                                            file_name)
        with open(downloaded_file_path, "wb") as f:
            f.write(response.content)
        print("File downloaded successfully.")

        # Extract the contents of the .zip file
        with zipfile.ZipFile(downloaded_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)
        print("File contents extracted successfully.")

        # Remove the downloaded .zip file
        os.remove(downloaded_file_path)
    else:
        print("Failed to download the file.")

def fetch_page_content(url):
    # Fetch the page content
    response = requests.get(url)
    if response.status_code == 200:
        # Use regular expression to find links to .zip files
        zip_links = re.findall(r'href=["\'](.*?\.zip)["\']', response.text)
        return zip_links
    else:
        print("Failed to fetch the page content.")


if __name__ == "__main__": pwd
PC_LOG_URL='http://10.41.24.125:9000/scheduled_deployments/2023-08-09/64d35cea82e14f1c567fdc0b/deployments/64d35cea82e14f1c567fdc0d/entity_logs/retry_0/10.37.110.39/'
#tar_download_and_extract(PC_LOG_URL)
#zip_download_and_extract(file_url=None)
#fetch_page_content()