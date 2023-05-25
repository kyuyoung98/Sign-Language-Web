from django.db import models
from django.contrib.auth.models import User

class UserChatResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    pub_date = models.DateTimeField('date published')