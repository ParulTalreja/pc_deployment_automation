import os
import pwd
import re
import subprocess
import zipfile

import requests


def download_pc_logs(PC_LOG_URL):
    zip_links=fetch_page_content(PC_LOG_URL)
    #if PC logs are in zip format
    if zip_links:
        downloaded_location=zip_download_and_extract(PC_LOG_URL)
    else:
        downloaded_location=tar_download_and_extract(PC_LOG_URL)
    return downloaded_location



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

def zip_download_and_extract(LOG_URL):
    # PE_LOG_URL:URL of the .zip file to download
    # Folder where you want to extract the contents
    extract_folder = "resources"

    # Create the extraction folder if it doesn't exist
    os.makedirs(extract_folder, exist_ok=True)

    zip_links=fetch_page_content(LOG_URL)
    if not zip_links:
        print("No Zip file available at url ",LOG_URL)
        return
    for zip_link in zip_links:
        file_url = LOG_URL+zip_link
        return(download_and_save_zip_file(file_url,extract_folder,zip_link))




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
        extract_folder_url=downloaded_file_path.replace(".zip", "")+"/cvm_logs"
        return extract_folder_url

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
        return None


#if __name__ == "__main__": pwd
#PC_LOG_URL='http://10.41.24.125:9000/scheduled_deployments/2023-08-25/64e910f773101a2e983cb067/deployments/64e910f773101a2e983cb06b/entity_logs/retry_0/10.37.109.88/logbay_PC-10.37.109.88_1693002714/'
#download_pc_logs(PC_LOG_URL)