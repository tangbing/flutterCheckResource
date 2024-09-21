#!/user/local/bin/python3
# 将本文件放在Flutter项目的根目录

from genericpath import isdir
from operator import delitem
import os
import re
from sys import path
import sys
from typing import List
from PIL import Image  # 使用Pillow代替imghdr进行图像检查
import chardet  # 用于检测文件编码

print("---分析未使用的资源文件----")
# 项目目录
projectAbsRootPath = sys.path[0]
# 图片所在的资源目录路径
assetPath = "/asset"
# 项目中dart代码所在目录
libPath = projectAbsRootPath + "/lib"
assetAbPath = projectAbsRootPath + assetPath

print("项目根路径:" + projectAbsRootPath + "   资源目录:" + assetAbPath + "     lib目录:" + libPath)
print("----------开始查找图片--------------")

# 使用Pillow判断文件是否为图片
def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            return img.format.lower() in {"jpg", "jpeg", "bmp", "png", "tiff"}
    except (IOError, OSError):
        return False

# 遍历目录，将图片路径存储到列表中的方法
def searchImage(filePath):
    list = []
    isDir = os.path.isdir(filePath)
    if isDir:
        for f in os.listdir(filePath):
            if f.startswith("."):
                print(filePath + "/" + f)
            else:
                tList = searchImage(filePath + "/" + f)
                list.extend(tList)
    else:
        if is_image(filePath):
            list.append(filePath)
    return list

# 项目中使用的图片资源路径集合
imageList = searchImage(assetAbPath)

print("-------------遍历dart文件，分析未使用的图片---------")

def matchAndDelImage(contentStr, list):
    for imgPath in list[:]:
        index = imgPath.find(assetPath)
        imgName = imgPath[index + 1:]
        match = re.search(imgName, contentStr)
        if match:
            list.remove(imgPath)

# 检测文件编码的方法
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

# 在Dart文件中查找图片使用情况的方法
def searchImageInDart(filePath, list):
    if os.path.isdir(filePath):
        for f in os.listdir(filePath):
            searchImageInDart(filePath + "/" + f, list)
    else:
        encoding = detect_encoding(filePath)
        with open(filePath, 'r', encoding=encoding, errors='ignore') as f:
            contentStr = f.read()
            if len(contentStr) != 0:
                matchAndDelImage(contentStr, list)

searchImageInDart(libPath, imageList)

print("------在dart文件中未找到被使用的图片如下-----数量:" + str(len(imageList)))
for img in imageList:
    print("可能未使用-->" + img)
    # os.remove(img)
print("-------------------分析完成-------------------------------")
