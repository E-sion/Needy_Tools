# 读取原始的txt文件
import os
import shutil
import re
from collections import defaultdict

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import openai

from Jines.Option import emoji_jsonl


def copy_files_with_content(source_directory, target_directory):
    for filename in os.listdir(source_directory):
        if filename.endswith(".txt"):
            with open(os.path.join(source_directory, filename), 'r', encoding="utf-8") as file:
                lines = file.readlines()
            if any("### Option-2" in line for line in lines) and any("Reply：" in line for line in lines):
                shutil.copy(os.path.join(source_directory, filename), target_directory)


# 小数转整数
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'(\d+)\.0\b', r'\1', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def process_directory(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.txt'):  # or whatever file type you're processing
                process_file(os.path.join(root, file))


import json




# 使用这个函数来处理你的JSONL文件
# emoji_jsonl('Daily_event_130.jsonl')

# process_directory('move')
# copy_files_with_content('events', 'move')
