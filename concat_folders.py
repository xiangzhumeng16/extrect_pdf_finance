import os
import shutil
import glob

def move_file(file_name, fold='error_fold'):
    if not os.path.exists(fold):
        os.mkdir(fold)
    dest_file = os.path.join(fold, os.path.basename(file_name))
    shutil.move(file_name, dest_file)
    print(f"Succefully moving the file {file_name} into the target {dest_file} file.")

def concat_folders(fold='error_fold'):
    for sub_dir in os.listdir(fold):
        for filename in glob.glob(os.path.join(fold, sub_dir)+'/*.txt'):
            if os.path.exists(filename):
                move_file(filename, fold=fold)
		os.removedirs(os.path.join(fold, sub_dir))

if __name__ == "__main__":
    # filter_errors()
    concat_folders('sample_2015_txt_split')
    
