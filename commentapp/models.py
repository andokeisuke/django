from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Commentモデルの定義
class Comment(models.Model):
    title = models.CharField(max_length=100)# タイトル
    text = models.TextField()# 本文
    date = models.DateTimeField(default=timezone.now())# 作成日
    create_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)# 作成者（ユーザテーブル参照の外部キー）

    IS_PUBLIC_CHOICES = (# 公開・非公開の選択肢定義
        (False, '非公開'),
        (True, '公開'),
    )
    is_public = models.BooleanField(default=True,choices=IS_PUBLIC_CHOICES)# 公開設定
    
    def __str__(self):
        return self.title

