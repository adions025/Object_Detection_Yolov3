"""
mAP
Written by Adonis Gonzalez & changed by Tom Doornbos :O
------------------------------------------------------------
"""
import sys
import os
from shutil import copyfile
import matplotlib.pyplot as plt
import numpy as np

#PATHS
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)

#folder1 = os.path.join(ROOT_DIR, "prueba1")
#dataset/train/tiles, dataset/test/tiles
tiles_folder = os.path.join(ROOT_DIR, "dataset/train/tiles")
#dataset/train/training, dataset/test/testset
training_folder = os.path.join(ROOT_DIR, "dataset/train/training")
#print(tiles_folder)

def read_txt_file(path):

    imgs_list = open(path + '/image.txt', 'r').readlines()
    return imgs_list

def list_dirs(path):
    subdirs = []
    for subdir in os.listdir(path):
        subdirs.append(subdir)
    return subdirs

def grabNamesImages(path):
  files = os.listdir(path)
  #print(files)
  with open(path + "/" + 'image.txt', 'w') as f:
    for item in files:
        if (item.endswith('.txt')):
            if item == "result.txt":
                None
            elif item =="image.txt":
                None
            else:
                f.write("%s\n" % item)
  f.close()
  #print("List of images, images.tx, was save in", path)


if __name__ == "__main__":
    subdirs = list_dirs(tiles_folder)


    for subdir in subdirs:
        subdir_fullpath = os.path.join(tiles_folder, subdir)
        sub_path = subdir_fullpath.strip().split('yolo3/')[-1]

        grabNamesImages(subdir_fullpath)
        image_txt_files = read_txt_file(subdir_fullpath)

        with open(training_folder + "/" + "final_results.txt", "a") as f:
            for txt in image_txt_files:
                img_name = txt.strip().split('/')[-1]
                name = open(subdir_fullpath + '/' + img_name, 'r').readlines()
                name_path = str(subdir_fullpath).split("yolo3/")[1]
                if (str(name).replace('(', '$').replace(')', '$').split('$')[2]):
                    name_anno_temp = str(name).strip().split(',')[0].replace('["','')
                    name_anno = str(name).strip().replace('(', '').replace(')','').replace('\\n"', '').replace(name_anno_temp,'').replace('[", ', '&').replace(']','&').split('&')[1]
                    if "Erosion" in name_anno:
                        name_anno = name_anno.replace("'Erosion'", '0$')
                    if "SD" in name_anno:
                        name_anno = name_anno.replace("'SD'", '1$')
                    if "B" in name_anno:
                        name_anno = name_anno.replace("'B", '2$')
                    if "Dirt" in name_anno:
                        name_anno = name_anno.replace("'Dirt'", '3$')
                    name_anno = str(name_anno.replace(" ","")).replace('0$,', '0 ').replace('1$,', '1 ').replace('2$,', '2 ').replace('3$,', '3 ').replace('0$', '0 ').replace('1$', '1 ').replace('2$', '2 ').replace('3$', '3 ')
                    print(name_path +'/'+str(img_name).replace('txt','jpg')+ ' ' + name_anno)
                f.write("%s\n" % str(name_path +'/'+str(img_name).replace('txt','jpg')+ ' ' + name_anno))


        for filename in (os.listdir(subdir_fullpath)):
            if (filename == "result.txt"):
                results = open(subdir_fullpath + '/' + filename, 'r').readlines()



            if filename.endswith('jpg'):
                fileparts = filename.split('.')
                copyfile(subdir_fullpath+"/"+filename,training_folder+"/"+filename)
