import os
import shutil

# Function to remove all files in a directory
def remove_and_renew(dir):
    shutil.rmtree(dir)
    os.makedirs(dir)

def main():

    input_dirs = ['./data/inputs/processed_data', './data/inputs/processed_data_vis']
    output_dir = './data/outputs'
    
    for dir in input_dirs:
        remove_and_renew(dir)

    remove_and_renew(output_dir)


if __name__ == '__main__':
    main()