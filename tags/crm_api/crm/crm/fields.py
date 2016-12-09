# -*- coding: utf-8 -*-

import os

from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image


def _add_thumb(s):
    """
    Modifies a string (filename, URL) containing an image filename, to insert
    '.thumb' before the file extension (which is changed to be '.jpg').
    例:"rabbit.jpg"上传后得到的预览文件名就是"rabbit.thumb.jpg"
    """
    parts = s.split('.')
    parts.insert(-1, 'thumb')
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return '.'.join(parts)


class ThumbnailImageFieldFile(ImageFieldFile):

    @property
    def _get_thumb_path(self):
        return _add_thumb(self.path)

    @property
    def _get_thumb_url(self):
        return _add_thumb(self.url)

    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)  # 打开原图片文件
        img.thumbnail((self.field.thumb_width, self.field.thumb_height), Image.ANTIALIAS)  # 创建预览
        img.save(self.thumb_path, 'JPEG')  # 将预览保存为预览文件名

    def delete(self, save=True):
        """首先获取预览文件名,如存在就删除它,然后父类删除它自己的文件(原图)"""
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField):
    """
    Behaves like a regular ImageField, but stores an extra (JPEG) thumbnail
    image, providing FIELD.thumb_url and FIELD.thumb_path.
    Accepts two additional, optional arguments: thumb_width and thumb_height,
    both defaulting to 128 (pixels). Resizing will preserve aspect ratio while
    staying inside the requested dimensions; see PIL's Image.thumbnail()
    method documentation for details.
    """
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
