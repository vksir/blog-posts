import datetime
import json
import os
import re
import yaml


class Post:
    METADATA_TITLE = 'title'
    METADATA_ID = 'id'
    METADATA_CATEGORIES = 'categories'
    METADATA_TAGS = 'tags'
    METADATA_DATE = 'date'
    METADATA_UPDATED = 'updated'

    TEXT_MORE = '<!-- more -->'
    TEXT_MORE_LINES = 8

    def __init__(self, path, filename, category, tags):
        self.path = path
        self.title = filename[:-3]
        self.category = category
        self.tags = tags

        self.content = self._read()
        self.metadata = ''
        self.text = ''

        self.metadata_id = ''

    def analyze(self):
        self._analyze_content()

    def _analyze_content(self):
        res = re.search(r'^---(.*?)---(.*)', self.content, re.S)
        if not res:
            self.metadata = '{}'
            self.text = self.content.strip('\n')
            return
        metadata, text = res.groups()
        self.metadata = metadata.strip('\n')
        self.text = text.strip('\n')

    def complete(self):
        self._complete_metadata()

        # 使用 hugo，不再需要 more 分割文章了
        # self._complete_text_more()

    def _complete_metadata(self):
        data = yaml.load(self.metadata, yaml.Loader)

        # title
        data.setdefault(self.METADATA_TITLE, self.title)
        # url
        data.setdefault(self.METADATA_ID, '')
        # category
        data[self.METADATA_CATEGORIES] = [self.category]
        # tags
        tags = data.get(self.METADATA_TAGS, [])
        data[self.METADATA_TAGS] = list(set(tag.lower() for tag in set(tags + self.tags)))
        data[self.METADATA_TAGS].sort()
        # date
        data.setdefault(self.METADATA_DATE, datetime.datetime.now())

        # hexo 使用 id 字段作为 url
        # hugo 使用 url 字段
        data['url'] = data['id']

        self.metadata = yaml.dump(data, allow_unicode=True)
        self.metadata_id = data[self.METADATA_ID]

    def _complete_text_more(self):
        self.text = re.sub(r'\n%s\n' % self.TEXT_MORE, '', self.text)

        lines = self.text.splitlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('```'):
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    i += 1
            if i >= self.TEXT_MORE_LINES:
                if not lines[i]:
                    lines.insert(i, '\n' + self.TEXT_MORE)
                    break
            i += 1
        self.text = '\n'.join(lines)

    def save(self):
        new_content = f'---\n' \
                      f'{self.metadata}' \
                      f'---\n' \
                      f'\n' \
                      f'{self.text}\n'
        self._write(new_content)

    def _read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return f.read()

    def _write(self, content):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(content)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return json.dumps({
            'path': self.path,
            'category': self.category,
            'tags': self.tags
        }, ensure_ascii=False)


class FileLib:
    REPO_DIR = os.path.dirname(__file__)
    POSTS_DIRNAME = 'content/posts'
    POSTS_DIR = os.path.join(REPO_DIR, POSTS_DIRNAME)

    @classmethod
    def _get_tags(cls, dirpath):
        new_dirpath, dirname = os.path.split(dirpath)
        if dirname == cls.POSTS_DIRNAME:
            return []
        return cls._get_tags(new_dirpath) + [dirname]

    @classmethod
    def get_posts(cls):
        posts = []
        categories = os.listdir(cls.POSTS_DIR)
        for category in categories:
            category_dir = os.path.join(cls.POSTS_DIR, category)
            for dirpath, _, filenames in os.walk(category_dir):
                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    tags = cls._get_tags(dirpath)
                    post = Post(path, filename, category, tags)
                    posts.append(post)
        return posts


def main():
    posts = FileLib.get_posts()
    for post in posts:
        post.analyze()
        post.complete()
        post.save()

    # 检查是否有文章 id 为空
    for post in posts:
        if post.metadata_id == '':
            raise Exception(f'empty post id: {post}')

    raw_metadata_ids = [post.metadata_id for post in posts]
    metadata_ids = set(raw_metadata_ids)
    if len(metadata_ids) != len(raw_metadata_ids):
        duplicate_ids = {}
        for medata_id in raw_metadata_ids:
            count = raw_metadata_ids.count(medata_id)
            if raw_metadata_ids.count(medata_id) > 1:
                duplicate_ids[medata_id] = count
        raise Exception(f'duplicate id: {len(metadata_ids)} != {len(raw_metadata_ids)}\n'
                        f'{json.dumps(duplicate_ids, indent=4)}')


if __name__ == '__main__':
    main()

