# 读取原始的txt文件
import os
import shutil
import re
from collections import defaultdict


def process_text(text):
    # 使用正则表达式匹配所有的Attribute Change
    matches = re.findall(r'(### Option-\d+.*?)(Attribute Change:.*?)(### Option-\d+|$)', text, re.DOTALL)

    new_text = ''
    for match in matches:
        option_text = match[0]
        attribute_changes = match[1].split('\n')
        attribute_changes = [change for change in attribute_changes if change.strip()]

        # 计算所有Attribute Change的总和
        total_changes = defaultdict(float)
        for change in attribute_changes:
            for attr in ['Affection', 'Stress', 'Darkness']:
                if attr in change:
                    total_changes[attr] += float(re.search(f'{attr}: (-?\d+\.?\d*)', change).group(1))

        # 移除原有的Attribute Change，并添加新的Attribute Change
        option_text = re.sub(r'Attribute Change:.*', '', option_text, flags=re.DOTALL)
        if total_changes:
            option_text += 'Attribute Change: ' + ' '.join(
                f'{attr}: {value}' for attr, value in total_changes.items()) + '\n'
        else:
            option_text += 'Attribute Change: None\n'

        new_text += option_text

    return new_text


def copy_files_with_content(source_directory, target_directory):
    for filename in os.listdir(source_directory):
        if filename.endswith(".txt"):
            with open(os.path.join(source_directory, filename), 'r',encoding="utf-8") as file:
                lines = file.readlines()
            if any("### Option-2" in line for line in lines) and any("Reply：" in line for line in lines):
                shutil.copy(os.path.join(source_directory, filename), target_directory)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    for line in lines:
        if 'Attribute Change: None' in line:
            skip = True
        elif 'Option-' in line and skip:
            skip = False
        if not skip:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def process_directory(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.txt'):  # or whatever file type you're processing
                process_file(os.path.join(root, file))

# process_directory('move')
copy_files_with_content('events', 'move')