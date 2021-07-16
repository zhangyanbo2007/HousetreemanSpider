from PIL import Image
import numpy as np
import os
import copy
import glob
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os, sys, types
from hashlib import md5
import os
from time import clock as now
import shutil


def is_valid(file):
    valid = True
    try:
        Image.open(file).load()
    except OSError:
        valid = False
    return valid


def is_jpg(file):
    try:
        i = Image.open(file)
        return i.format =='JPEG'
    except IOError:
        return False


def is_small(file, threshold=200):
    try:
        i = Image.open(file)
        if i.size[0] < threshold or i.size[1] < threshold:
            return True
        else:
            return False
    except IOError:
        return False


def is_gray(img, color_threshold=70, grey_threshold=50):
    if len(img.getbands()) != 1:
        # 彩色图
        img1 = np.asarray(img.getchannel(channel=0), dtype=np.int16)
        img2 = np.asarray(img.getchannel(channel=1), dtype=np.int16)
        img3 = np.asarray(img.getchannel(channel=2), dtype=np.int16)
        diff1 = (img1 - img2).var()
        diff2 = (img2 - img3).var()
        diff3 = (img3 - img1).var()
        diff_sum = (diff1 + diff2 + diff3) / 3.0
        if diff_sum >= color_threshold:
            return "with_color"
        else:
            return "with_color_but_grey"
    else:
        # 灰度图
        grey_min = np.asarray(img.getchannel(channel=0), dtype=np.int16).min()
        if grey_min < grey_threshold:
            return "grey_color"
        else:
            return "grey_except_color"


def cmpandremove(path):
    def getmd5(filename):
        file_txt = open(filename, 'rb').read()
        m = md5(file_txt)
        return m.hexdigest()
    start = now()
    all_md5 = []
    total_file = 0
    total_delete = 0
    for file in os.listdir(path):
        total_file += 1
        real_path = os.path.join(path, file)
        if os.path.isfile(real_path):
            filemd5 = getmd5(real_path)
            if filemd5 in all_md5:
                total_delete += 1
                os.remove(real_path)
                print(u'删除', file)
            else:
                all_md5.append(filemd5)
    end = now()
    time_last = end - start
    print(u'文件总数：', total_file)
    print(u'删除个数：', total_delete)
    print(u'耗时：', time_last, u'秒')


if __name__ == "__main__":
    path = "data/sougou_treeman"
    _, path_name = os.path.split(path)
    cmpandremove(path)
    output_path = f"data/result/{path_name}_result"

    grey_except_color_dir = os.path.join(output_path, "grey_except_color")
    grey_color_dir = os.path.join(output_path, "grey_color")
    with_color_dir = os.path.join(output_path, "with_color")
    with_color_but_grey_dir = os.path.join(output_path, "with_color_but_grey")
    no_valid_dir = os.path.join(output_path, "no_valid")
    small_dir = os.path.join(output_path, "small")
    img_dict = {}
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)
    if not os.path.exists(grey_except_color_dir):
        os.mkdir(grey_except_color_dir)
    if not os.path.exists(with_color_dir):
        os.mkdir(with_color_dir)
    if not os.path.exists(with_color_but_grey_dir):
        os.mkdir(with_color_but_grey_dir)
    if not os.path.exists(grey_color_dir):
        os.mkdir(grey_color_dir)
    if not os.path.exists(no_valid_dir):
        os.mkdir(no_valid_dir)
    if not os.path.exists(small_dir):
        os.mkdir(small_dir)
    for file in glob.glob(f"{path}/*.jp*g"):
        try:
            img_src = Image.open(file)
        except Exception as e:
            continue
        if is_valid(file) and is_jpg(file):
            if is_small(file):
                os.system(f"cp {file} {small_dir}")
                # print("small")
            elif is_gray(img_src) != "with_color":
                if is_gray(img_src) == "grey_color":
                    os.system(f"cp {file} {grey_color_dir}")
                    # print("grey_color")
                elif is_gray(img_src) == "with_color_but_grey":
                    os.system(f"cp {file} {with_color_but_grey_dir}")
                    # print("with_color_but_grey")
                else:
                    os.system(f"cp {file} {grey_except_color_dir}")
                    # print("grey_except_color")
            else:
                os.system(f"cp {file} {with_color_dir}")
                # print("with_color")
        else:
            os.system(f"cp {file} {no_valid_dir}")
            # print("no_valid")