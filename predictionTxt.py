import os
import sys
import xml.etree.ElementTree as ET

from yolo import YOLO, detect_video
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageColor

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)

mAP_gt = os.path.join(ROOT_DIR, 'mAP/input/ground-truth/')
mAP_dr = os.path.join(ROOT_DIR, 'mAP/input/detection-results')
#test-set
test = os.path.join(ROOT_DIR, 'test/testset')
path = os.path.join(ROOT_DIR, 'test/')

def grab_images(path):
    files = os.listdir(path)
    with open(path + '/image.txt', 'w+') as f:
        for name in files:
            if (name.endswith('.jpg')):
                f.write("%s\n" % name)
    f.close()
    print("List of images, images.tx, was save in", path)
    print("-------------------------------------------")
    print("--INFO IMAGE                             --")
    print("-------------------------------------------")

def saving_only_ground_truth(path, img, img_name, xmin, ymin, xmax, ymax, color='black', thickness=4):
    draw = ImageDraw.Draw(img)
    (left, top, right, bottom) = (int(xmin), int(ymin), int(xmax), int(ymax))
    print(left, top, right, bottom)

    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)

    del draw

    name = (path + "/results/" + "ground_truth_" + img_name)
    print(img_name)
    img.save(name, "JPEG")

    print("-------tommy--------")
    print("saving image")

def cleaner(dir_name):
    remove = os.listdir(dir_name)

    for item in remove:
        if item.endswith(".txt"):
            os.remove(os.path.join(dir_name, item))

def load_image(filename):
    try:
        img = Image.open(filename)
        print("(H, W, D) = (height, width, depth)")
    except Exception as e:
        print(e)
        print ("Unable to load image")

    return img.size, img

def create_gt(name_img, name_damage, xmin, ymin, xmax, ymax, path):
    print(name_img + '.txt', name_damage, (xmin, xmax), (ymin, ymax))
    f = open(path + name_img + ".txt", "a+")
    f.write(name_damage +' '+ str(xmin) +' '+ str(xmax) +' '+ str(ymin) +' '+ str(ymax) + '\n')
    f.close()

if __name__ == "__main__":
    cleaner(mAP_gt)
    cleaner(mAP_dr)
    #yolo = YOLO()
    grab_images(test)
    txt_list = open(test + '/final_result.txt', 'r').readlines()
    for line in txt_list:
        for note in line.strip().split(' '):
            if "dataset" in note:
                img = note
                img_name = note.strip().split('/')[-1]
                filename = (test + '/' + img_name)
                img_shape, img = load_image(filename)
                only_img = (img_name.strip().split('.jpg')[0])
                #image, box = yolo.detect_image(img, only_img)
            elif "dataset" not in note:
                xmin, ymin, xmax, ymax, name_damage = note.split(',')
                #print(img_name, xmin, ymin, xmax, ymax, name_damage)
                #create_gt(only_img, name_damage, xmin, xmax, ymin, ymax, mAP_gt)
                saving_only_ground_truth(path, img, img_name, xmin, ymin, xmax, ymax, '#ff0000', thickness=10)
                #print(name_damage)
    #print(imgs_list)
    '''
    imgs_list = open(test + '/image.txt', 'r').readlines()
    for img in imgs_list:
        print("image list")
        print(img)
        print(imgs_list.index(img))

        img_name = img.strip().split('/')[-1]
        filename = (test + '/' + img_name)
        img_shape, img = load_image(filename)

        only_img = (img_name.split('.jpg')[0])
        xml_n = only_img + '.xml'

        image, box = yolo.detect_image(img, only_img)

        tree = ET.ElementTree(file=test + '/' + xml_n)
        root = tree.getroot()
        xmin, xmax, ymin, ymax = {}, {}, {}, {}
    '''

        #create_gt(only_img, name_damage, xmin, xmax, ymin, ymax, mAP_gt)
        #saving_only_ground_truth(test, img, img_name, xmin, xmax, ymin, ymax, '#ff0000', thickness=10)