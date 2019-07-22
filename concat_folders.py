import os
import shutil
import glob

def error_files_management(file_name, fold='error_fold'):
    if not os.path.exists(fold):
        os.mkdir(fold)
    dest_file = os.path.join(fold, os.path.basename(file_name))
    shutil.move(file_name, dest_file)
    print(f"Succefully moving the file {file_name} into the target {dest_file} file.")

def filter_errors(fold='error_fold'):
    for sub_dir in os.listdir(fold):
        for filename in glob.glob(os.path.join(fold, sub_dir)+'/*.txt'):
            if os.path.exists(filename):
                error_files_management(filename, fold=fold)

if __name__ == "__main__":
    # filter_errors()
    filter_errors('sample_2015_txt_split')
    