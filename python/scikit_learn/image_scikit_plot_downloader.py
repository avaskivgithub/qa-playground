"""
1. Download png images from https://scikit-learn.org/stable/user_guide.html
2. Generate your own test plot
3. Look up test plot in the downloaded images from #1
Potentially to simplify matching process
"""
import requests
from bs4 import BeautifulSoup
import os
import base64

IMG_DIR_NAME = "images"
CWD_DIR_PATH = os.getcwd()
# File to save the href values
ALL_HREF_FILE_NAME = "href_list.txt"
# URL of the webpage
url_base = "https://scikit-learn.org/stable"

# Create a folder to save images
os.makedirs(IMG_DIR_NAME, exist_ok=True)

def download_urls_from_scikit_learn_single_page(href,
                                                dest_dir_path=os.path.join(CWD_DIR_PATH, IMG_DIR_NAME)):
    url = f"{url_base}/{href}"
    print(url)
    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all image tags
    img_tags = soup.find_all("img", src=True)
    # print(img_tags)

    # Download and save each image
    for img_tag in img_tags:
        if 'base64,' in img_tag:
            string = img_tag.split('base64,')[1]
            decoded = base64.decodebytes(string.encode("ascii"))

            # Save the image
            img_name = f'{img_tag[-10:]}.png'
            with open(f"{dest_dir_path}/{img_name}", "wb") as img_file:
                img_file.write(decoded)
        else:
            img_url = url_base + img_tag.get("src").split('..')[-1]
            if img_url:
                # Handle relative URLs
                if not img_url.startswith("http"):
                    img_url = f"https://scikit-learn.org{img_url}"
                
                # Fetch the image
                # print(img_url)
                try:
                    response = requests.get(img_url)
                    img_data = response.content

                    # Save the image
                    img_name = os.path.basename(img_url)
                    with open(f"{dest_dir_path}/{img_name}", "wb") as img_file:
                        img_file.write(img_data)
                    # print(f"Downloaded: {img_name}")
                except Exception as e:
                    print(str(e))

    print(f"All images have been downloaded from {href} into {dest_dir_path}!")

def get_all_hrefs_from_scikit_learn(url, delimiter=':::'):

    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Open the output file to save href values
    with open(ALL_HREF_FILE_NAME, "w") as file:
        # Find all <a> tags with text
        for a_tag in soup.find_all("a"):
            href = a_tag.get("href")  # Extract href attribute
            text = a_tag.get_text(strip=True)  # Extract the visible text
            if href and text:  # Check if both href and text exist
                file.write(f"{text}{delimiter}{href}\n")
                print(f"Saved: {text} - {href}")

    print(f"All href values with text have been saved to '{ALL_HREF_FILE_NAME}'.")

def download_all_pages(url,
                       prnt_dest_dir_path=os.path.join(CWD_DIR_PATH, IMG_DIR_NAME)):
    delimiter=':::'
    get_all_hrefs_from_scikit_learn(url, delimiter=delimiter)

    with open(ALL_HREF_FILE_NAME, "r") as file:
        for line in file:
            crnt_dir_name, href = line.split(delimiter)
            crnt_dir_name = crnt_dir_name.replace(' ', '_')
            
            crnt_dir_path = os.path.join(prnt_dest_dir_path, crnt_dir_name)
            href = href.replace('\n', '')

            if not ('#' in href):
                try:
                    os.makedirs(crnt_dir_path)
                except Exception as er:
                    pass
                    # print(str(er))

                # run blocking function in another thread,
                # and wait for it's result:
                download_urls_from_scikit_learn_single_page(href=href, dest_dir_path=crnt_dir_path)
                # print(f'\ndownload_urls_from_scikit_learn_single_page(href={href}, dest_dir_path={crnt_dir_path})')

if __name__ == '__main__':

    url = f"{url_base}/user_guide.html"
    download_all_pages(url, prnt_dest_dir_path=os.path.join(CWD_DIR_PATH, IMG_DIR_NAME))

    # Example of getting imgs from one page
    # 1.1. Linear Models:::modules/linear_model.html
    # download_urls_from_scikit_learn_single_page(href='modules/linear_model.html')