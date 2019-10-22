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

    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)

    del draw

    name = (path + "/results/" + img_name)
    print(img_name)
    img.save(name, "JPEG")

    print("-------tommy--------")
    print("saving image")

def calculation_overlap(test, img ,xmin, xmax, ymin, ymax, box, color='#000000', thickness=20):
    top, left, bottom, right = box
    p_x_max = min(right, xmax)
    p_x_min= max(left, xmin)
    p_y_max = min(bottom, ymax)
    p_y_min = max(top, ymin)

    tmp_p_w = min(right, xmax) - max(left, xmin)
    tmp_p_h = min(bottom, ymax)- max(top, ymin)

    w_ann = xmin-xmax
    h_ann = ymin - ymax

    w_pre =left-right
    h_pre =top-bottom

    predic_area = w_pre * h_pre
    annot_area = (w_ann * h_ann)
    overlap_area = (tmp_p_w * tmp_p_h)

    overlap = (float(overlap_area) / float(annot_area))
    total_overlapping = (overlap * 100)
    print("Total overlaping " + str(total_overlapping))

    draw = ImageDraw.Draw(img)

    draw.line([(p_x_min, p_y_min), (p_x_min, p_y_max), (p_x_max, p_y_max),
               (p_x_max, p_y_min), (p_x_min, p_y_min)], width=thickness, fill=color)
    del draw


    return overlap_area, annot_area, predic_area

def drawing_overlapping_area(path, img ,xmin, xmax, ymin, ymax, box, color='#ffff00', thickness=10):
    top, left, bottom, right = box
    p_x_max = min(right, xmax)
    p_x_min= max(left, xmin)
    p_y_max = min(bottom, ymax)
    p_y_min = max(top, ymin)

    draw = ImageDraw.Draw(img)
    (left, right, top, bottom) = (p_x_min, p_x_max, p_y_min, p_y_max)

    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)
    del draw


def drawing_union_area(path, img ,xmin, xmax, ymin, ymax, box, name, color='#FFC0CB', thickness=10):
    top, left, bottom, right = box
    u_xmax = max(right, xmax )
    u_xmin = min(left, xmin )
    u_ymax = max(bottom, ymax)
    u_ymin = min(top, ymin)

    tmp_p_w =  u_xmin - u_xmax
    tmp_p_h =  u_ymin - u_ymax

    total_are_of_union = tmp_p_w * tmp_p_h

    draw = ImageDraw.Draw(img)
    (left, right, top, bottom) = (u_xmin, u_xmax, u_ymin, u_ymax)


    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)

    del draw
    print("---------------------------------------------------")
    print("total area of union " + str(total_are_of_union))
    print("---------------------------------------------------")
    name = (path + "/results/" + "tommy" + ".jpg")
    img.save(name, "JPEG")

    return total_are_of_union

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

        #image, box = yolo.detect_image(img, only_img)

        tree = ET.ElementTree(file=test + '/' + xml_n)
        root = tree.getroot()
        xmin, xmax, ymin, ymax = {}, {}, {}, {}

        for child_of_root in root:
            if child_of_root.tag == 'object':
                for child_of_object in child_of_root:
                    if child_of_object.tag == 'name':
                        category_id = child_of_object.text
                        name_damage = (category_id.split(' ')[0])  # just for use SD intead SD1 levels
                        print("------------------")
                        print("INFO-ANNOTATION")
                        print("------------------")
                        print("this is the damage: ", name_damage)
                    if child_of_object.tag == 'bndbox':
                        for child_of_root in child_of_object:
                            if child_of_root.tag == 'xmin':
                                xmin = int(child_of_root.text)
                                print("this is de xmin: ", xmin)

                            if child_of_root.tag == 'xmax':
                                xmax = int(child_of_root.text)
                                print("this is de xmax: ", xmax)

                            if child_of_root.tag == 'ymin':
                                ymin = int(child_of_root.text)
                                print("this is de ymin: ", ymin)

                            if child_of_root.tag == 'ymax':
                                ymax = int(child_of_root.text)
                                print("this is de ymax: ", ymax)

                #create_gt(only_img, name_damage, xmin, xmax, ymin, ymax, mAP_gt)
                print(test, img, img_name, xmin, ymin, xmax, ymax)
                saving_only_ground_truth(path, img, img_name, xmin, ymin, xmax, ymax, '#ffff00', thickness=10)
'''              
                #bb_intersection_over_union(xmin, xmax, ymin, ymax, box)
                total_overlapping = calculation_overlap(test, img, xmin, xmax, ymin, ymax, box, '#000000', thickness=20)
                overlap_area, annot_area, predic_area = calculation_overlap(test, img, xmin, xmax, ymin, ymax, box, '#000000', thickness=20)
                #drawing_overlapping_area(test, img, xmin, xmax, ymin, ymax, box, '#ffff00', thickness=10)
                #drawing_union_area(test, img, xmin, xmax, ymin, ymax, box, only_img, '#FFC0CB', thickness=10)

            # print("IoU : ",(total_overlapping/ total_are_of_union))
            total_area_of_union = (annot_area + predic_area - overlap_area)
            iou = (overlap_area / total_area_of_union)

            print("---------------------")
            print("IoU: ", iou)
            print("---------------------")
'''