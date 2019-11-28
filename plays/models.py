from django.db import models
from datetime import datetime

class Photo(models.Model):
    # file = models.FileField('ファイル')
    image = models.ImageField(upload_to='plays')
    created_at = models.DateTimeField('作成日時', null=False, default=datetime.now())
    tag_name = models.TextField('タグ名称', null=True)
    tag_ruby = models.TextField('タグ振り仮名', null=True)

    # def __str__(self):
    #     return self.image.url
