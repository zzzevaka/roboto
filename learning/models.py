from django.db import models


class LearningModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    file = models.FileField(upload_to='learning_models/')
    time = models.DateTimeField(auto_now=True)
