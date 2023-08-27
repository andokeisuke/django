from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.



class Comment(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now(), help_text='作成日')   
    create_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

    IS_PUBLIC_CHOICES = (
        (False, '非公開'),
        (True, '公開'),
    )
    is_public = models.BooleanField(default=True,choices=IS_PUBLIC_CHOICES)


    def __str__(self):
        return self.title

