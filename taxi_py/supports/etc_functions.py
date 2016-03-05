from __future__ import division
import os, shutil

def remove_creat_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    
def get_all_csv_files(path):
    return [fn for fn in os.listdir(path) if fn.endswith('.csv')]