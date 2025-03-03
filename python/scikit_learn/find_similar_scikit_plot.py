"""
1. Download png images from https://scikit-learn.org/stable/user_guide.html
2. Generate your own test plot
3. Look up test plot in the downloaded images from #1
Potentially to simplify matching process
"""
import requests
from bs4 import BeautifulSoup
from DeepImageSearch import Load_Data, Search_Setup
import os
import shutil

dir_name = "images"
current_dir = os.getcwd()
# URL of the webpage
url_base = "https://scikit-learn.org/stable"

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Create a folder to save images
os.makedirs(dir_name, exist_ok=True)

def download_urls_from_scikit_learn_page(href):
    url = f"{url_base}/{href}"
    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all image tags
    img_tags = soup.find_all("img")

    # Download and save each image
    for img_tag in img_tags:
        img_url = url_base + img_tag.get("src").split('..')[-1]
        if img_url:
            # Handle relative URLs
            if not img_url.startswith("http"):
                img_url = f"https://scikit-learn.org{img_url}"
            
            # Fetch the image
            print(img_url)
            try:
                response = requests.get(img_url)
                img_data = response.content
                
                # Save the image
                img_name = os.path.basename(img_url)
                with open(f"images/{img_name}", "wb") as img_file:
                    img_file.write(img_data)
                print(f"Downloaded: {img_name}")
            except Exception as e:
                print(str(e))

    print("All images have been downloaded!")

def get_all_hrefs_from_scikit_learn(url):

    # File to save the href values
    output_file = "href_list.txt"

    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Open the output file to save href values
    with open(output_file, "w") as file:
        # Find all <a> tags with text
        for a_tag in soup.find_all("a"):
            href = a_tag.get("href")  # Extract href attribute
            text = a_tag.get_text(strip=True)  # Extract the visible text
            if href and text:  # Check if both href and text exist
                file.write(f"{text}: {href}\n")
                print(f"Saved: {text} - {href}")

    print(f"All href values with text have been saved to '{output_file}'.")

def find_similar_images(dir_path, img_path):
    # pip install DeepImageSearch --upgrade

    # Load images from a folder
    image_list = Load_Data().from_folder([os.path.join(dir_path, dir_name)])
    print(image_list[:5])

    # https://timm.fast.ai/ - for list of models
    # Set up the search engine, You can load 'vit_base_patch16_224_in21k', 'resnet50' etc more then 500+ models 
    st = Search_Setup(image_list=image_list, model_name='vgg19', pretrained=True, image_count=100)

    # Index the images
    st.run_index()

    # Get metadata
    # metadata = st.get_image_metadata_file()
    # print(metadata[:5])

    # Get similar images
    result = st.get_similar_images(image_path=os.path.join(dir_path, img_path), number_of_images=2)
    # print(list(result.values()))

    # Plot similar images
    # st.plot_similar_images(image_path=os.path.join(dir_path, img_path), number_of_images=3)
    return list(result.values())

if __name__ == '__main__':

    url = f"{url_base}/user_guide.html"
    # get_all_hrefs_from_scikit_learn(url)
    # TOBD: go through each page and generate plot and look it up in the list of downloaded plots

    # Example of getting imgs from one page
    download_urls_from_scikit_learn_page(href='modules/linear_model.html')

    # Test comparing plots with copy file
    test_file_name = 'sphx_glr_plot_ridge_path_001.png'
    test_copy_file_name = f'copy_{test_file_name}'
    shutil.copy(os.path.join(current_dir, dir_name, test_file_name),
                os.path.join(current_dir, test_copy_file_name))
    
    similar_files = find_similar_images(current_dir, test_copy_file_name)
    print(f'Similar images: {similar_files}')

    