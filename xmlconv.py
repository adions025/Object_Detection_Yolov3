import sys
import xml.etree.ElementTree as ET
import os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)
annotation = os.path.join(ROOT_DIR, 'annotation')

file = open('output.txt','w')
for anno in os.listdir(annotation):
    if anno.endswith('.jpg'):
        tree = ET.parse('annotation/' + anno)
        root = tree.getroot()
        filename = 'images/' + root.find('filename').text
        name = root.find('object').find('name').text
        print(filename)
        file.write(filename + ' ')
        for object in root.iter('object'):
            xmin = object.find('bndbox').find('xmin').text
            ymin = object.find('bndbox').find('ymin').text
            xmax = object.find('bndbox').find('xmax').text
            ymax = object.find('bndbox').find('ymax').text
            name = object.find('name').text
            if 'Erosion' in name:
                name = '0'
            if 'SD' in name:
                name = '1'
            if 'B&C' in name:
                name = '2'
            if 'Dirt' in name:
                name = '3'
            file.write(xmin + ','+ ymin + ','+ xmax + ','+ ymax + ','+ name + ' ')
        file.write("\n")
    file.close()