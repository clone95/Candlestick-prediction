import os
 
def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        print(f'Making folder: {directory}')
        os.makedirs(directory)

