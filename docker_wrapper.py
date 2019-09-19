#!/usr/bin/python3
# coding=utf8
# utf8 without BOM

import os
import sys
import logging

MAP_DICT = {'gcr.io': 'gcr.azk8s.cn', 'k8s.gcr.io': 'gcr.azk8s.cn/google-containers', 'quay.io': 'quay.azk8s.cn'}


def execute_sys_cmd(cmd):
    result = os.system(cmd)
    if result != 0:
        logging.info(cmd + " failed.")


def usage():
    print("Usage: " + sys.argv[0] + " pull ${image}")


def pull_and_tag_image(image):
    image = image.strip()
    image_array = image.split('/')
    new_image = ''
    if MAP_DICT.get(image_array[0], 0):
        new_image = image.replace(image_array[0], MAP_DICT.get(image_array[0]))
    if new_image:
        print("-- pull {image} from {new_image} instead --".format(image=image, new_image=new_image))
        cmd = "docker pull {image}".format(image=new_image)
        execute_sys_cmd(cmd)

        cmd = "docker tag {new_image} {image}".format(new_image=new_image, image=image)
        execute_sys_cmd(cmd)

        cmd = "docker rmi {new_image}".format(new_image=new_image)
        execute_sys_cmd(cmd)

        print("-- pull {image} done --".format(image=image))
    else:
        cmd = "docker pull {image}".format(image=image)
        execute_sys_cmd(cmd)


def pull_images_list_from_file(images_list_path):
    if not os.path.exists(images_list_path):
        print("the images list path {} not exists".format(images_list_path))
        sys.exit(-1)
    with open(images_list_path, mode='r', encoding='utf-8') as f:
        for i in f.readlines():
            if i:
                pull_and_tag_image(i)


if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        usage()
        sys.exit(-1)

    if sys.argv[2] == '-r':
        images_list_path = sys.argv[3]
        pull_images_list_from_file(images_list_path)

    else:
        image = sys.argv[2]
        pull_and_tag_image(image)

    print("Pull all images completed")
    sys.exit(0)
