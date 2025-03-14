"""
1. Download png images from https://scikit-learn.org/stable/user_guide.html
2. Generate your own test plot
3. Look up test plot in the downloaded images from #1
Potentially to simplify matching process
"""
from DeepImageSearch import Load_Data, Search_Setup
import numpy as np
import os

from image_generator import generate_test_image
from image_scikit_plot_downloader import download_all_pages, IMG_DIR_NAME, CWD_DIR_PATH, url_base

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def list_folders_recursively(root_dir):
    folders = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            folders.append(folder_path)
    return folders

def find_similar_images(imgs_dir_path, img_path):
    # pip install DeepImageSearch --upgrade

    # Load images from a folder
    folders = list_folders_recursively(imgs_dir_path)
    image_list = Load_Data().from_folder(folders)
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
    result = st.get_similar_images(image_path=img_path, number_of_images=2)
    # print(list(result.values()))

    # Plot similar images
    # st.plot_similar_images(image_path=img_path, number_of_images=3)
    return list(result.values())

if __name__ == '__main__':

    # 1. Download all images
    # download_all_pages(f"{url_base}/user_guide.html", prnt_dest_dir_path=os.path.join(CWD_DIR_PATH, IMG_DIR_NAME))
    
    # 2. Generate test image
    test_file_name = 'sphx_glr_plot_ridge_path_001.png'
    test_copy_file_name = f'copy_{test_file_name}'
    
    generate_test_image(x = np.arange(-10, 11, 1),
                        f = lambda x: 2 * x, 
                        file_path=os.path.join(CWD_DIR_PATH, test_copy_file_name))
    
    # 3. Find image that is closest to image from step #2
    similar_files = find_similar_images(imgs_dir_path=os.path.join(CWD_DIR_PATH, IMG_DIR_NAME), 
                                        img_path=os.path.join(CWD_DIR_PATH, test_copy_file_name))
    print(f'Similar images: {similar_files}')

    