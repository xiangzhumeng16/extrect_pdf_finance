import os
import shutil

def error_files_management(file_name):
    if not os.path.exists('error_fold'):
        os.mkdir('error_fold')
    dest_file = os.path.join('./error_fold/', file_name.split('\\')[-1])
    shutil.move(file_name, dest_file)
    print(f"Succefully moving the file {file_name} into the target {dest_file} file.")

def filter_errors(errfile='error.txt'):
    filenames = open('error.txt').readlines()
    for filename in filenames:
        filename = filename.strip('\n')[:-4]+'.txt'
        print(filename)
        if os.path.exists(filename):
            error_files_management(filename)

if __name__ == "__main__":
    filter_errors()