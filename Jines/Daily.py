import json
import re
import shutil


def generateReplyUser(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    decoder = json.JSONDecoder()
    img_list = []
    # 读取每一列的jsonl内容
    for i in range(len(lines)):
        # 获取当前jsonl内容的text字段
        objs = []
        s = lines[i]
        while s:
            obj, pos = decoder.raw_decode(s)
            objs.append(obj)
            s = s[pos:].lstrip()
            for obj in objs:
                text = obj['img_name']
                img_list.append(text)

    with open('image_text_relationship_reply.jsonl', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            str_ = lines[i]
            user = re.search(r'"user": "(.*?)"', str_).group(1)
            reply = re.search(r'"reply": "(.*?)"', str_).group(1)
            print(
                '{"prefix": "", "options": [{"user": "%s", "reply": "%s", "attribute_change": ""}], "id": "", "category": "", "condition": "","img_name": "%s"}' % (
                    user, reply, img_list[i]))


from PIL import Image
import os
import imagehash


def find_similar_images(small_images_dir, large_images_dir, output_dir):
    # 存储小图片的哈希值
    small_images_hashes = {}

    # 遍历小图片目录，计算每张图片的哈希值
    for dirpath, dirnames, filenames in os.walk(small_images_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):  # 确保是文件，不是目录
                with Image.open(filepath) as img:
                    hash_val = imagehash.average_hash(img)
                    small_images_hashes[filename] = hash_val

    # 遍历大图片目录，找到与小图片相似的图片
    for dirpath, dirnames, filenames in os.walk(large_images_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):  # 确保是文件，不是目录
                with Image.open(filepath) as img:
                    hash_val = imagehash.average_hash(img)
                    # 比较大图片的哈希值与小图片的哈希值
                    for small_image, small_hash in small_images_hashes.items():
                        if hash_val - small_hash < 5:  # 哈希值差异小于5的图片被认为是相似的
                            print(f'大图片 {filename} 与小图片 {small_image} 相似')
                            # 复制相似的大图片到输出目录
                            shutil.copy2(filepath, output_dir)

# 使用你的图片目录路径替换 'path_to_small_images' 和 'path_to_large_images'
find_similar_images('image', 'NeedyAssets','similar_image')

# generateReplyUser(r'image_text_relationship.jsonl')

import json
