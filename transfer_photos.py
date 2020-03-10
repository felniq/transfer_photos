#!/usr/bin/env python3

'''
Import photos from SD card into folder with exif date from source file
In the end opens the folder where the last picture was transferred (windows).
forked from JohannesNE/importphotos
Use: python transfer_photos.py
'''

import os
import sys
import shutil
import subprocess
from PIL import Image
from datetime import datetime

# Insert appropriate path and files extention.
sd_photo_folder = 'G:\\DCIM\\100CANON\\' # example: '/media/mycard/disk/DCIM/'
base_folder = 'E:\\Google Kuvat\\'
file_extension = '.JPG' # example: '.ORF', '.jpg' or '.CR2'


def get_date_taken(path):
    image_date = Image.open(path)._getexif()[36867]
    image_date = image_date[:10]
    date_time_object = datetime.strptime(image_date, '%Y:%m:%d')
    image_date = date_time_object.strftime('%d.%m.%Y').replace(".0", ".").lstrip("0") + ' ' + ' '.join(args)
    return image_date


# Print iterations progress
# From this SO answer: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/15862022
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


args = sys.argv[1:]


def try_create_folder(output_folder_create):
    try:
        os.makedirs(output_folder_create)
    except FileExistsError as exists:
        None


def check_if_file_exists(_list):
    new_list = []
    for _file in _list:
        source_file = os.path.join(sd_photo_folder, _file)
        source_file_date = get_date_taken(source_file)
        destination_folder = os.path.join(base_folder, source_file_date.strip())
        try_create_folder(destination_folder)
        if os.path.exists(os.path.join(destination_folder, _file)):
            pass
        else:
            new_list.append(_file)
    return new_list


sd_files = os.listdir(sd_photo_folder)
#Filter for raw extension
selected_files = [k for k in sd_files if k.endswith(file_extension)]
selected_files = check_if_file_exists(selected_files)

#Copy files
#Progress bar
n_files = len(selected_files)
if n_files == 0:
    print("no images to transfer, exiting...")
    quit()

print('Copying', n_files, 'files to', base_folder)

printProgressBar(0, n_files, prefix = 'Copying photos:', suffix = '', length = 50)

for i, file_name in enumerate(selected_files):
    file_to_be_copied = os.path.join(sd_photo_folder, file_name)
    file_date = get_date_taken(file_to_be_copied)
    output_folder = os.path.join(base_folder, file_date.strip())
    file_at_destination = os.path.join(output_folder, file_name)
    try:
        printProgressBar(i + 1, n_files, prefix='Progress:', suffix='', length=50)
        shutil.copy2(file_to_be_copied, output_folder)
    except Error as err:
        print(err)

subprocess.Popen(f"explorer {output_folder}")