from django.db import models
from django.utils.functional import cached_property
from learning.utils import KerasModelMixin


class LearningModel(models.Model, KerasModelMixin):

    TYPE_KERAS = 0
    TYPE_CHOICES = (
        (TYPE_KERAS, 'keras'),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    file = models.FileField(upload_to='learning_models/', null=True)
    time = models.DateTimeField(auto_now=True)

    @cached_property
    def model(self):
        if self.type == self.TYPE_KERAS:
            return self.retrieve_keras_model()

    def __clear_model_cache(self):
        try:
            del self.__dict__['model']
        except KeyError:
            pass

    def save_model(self, model):
        if self.type == self.TYPE_KERAS:
            self.save_keras_model(model)
        self.__clear_model_cache()
