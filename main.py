import os
import re
import time


REPO_DIR = os.path.dirname(__file__)
POSTS_DIR = os.path.join(REPO_DIR, 'posts')


def deal_with_post(path, category, tag):
    print(path, category, tag)
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    data = re.sub(r'comments:\s*?(false|true).*?\n', '', data, re.S)
    data = re.sub(r'(?<=categories:\n).*?\n(?=\S)', f'  - {category}\n', data, re.S)
    data = re.sub(r'\n*<!-- more -->\n*', '\n\n', data, re.S)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


for root, dir_lst, file_lst in os.walk(POSTS_DIR):
    for file in file_lst:
        dirname, name_2 = os.path.split(root)
        _, name_1 = os.path.split(dirname)

        if name_1 != 'posts':
            category, tag = name_1, name_2
        else:
            category, tag = name_2, name_2
        deal_with_post(os.path.join(root, file), category, tag)
