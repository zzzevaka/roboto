from django.db import models
from django.utils.functional import cached_property
from learning.keras_utils import KerasModelMixin


class LearningModel(models.Model, KerasModelMixin):

    TYPE_KERAS = 0
    TYPE_CHOICES = (
        (TYPE_KERAS, 'keras'),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    file = models.FileField(upload_to='learning_models/', blank=True)
    time = models.DateTimeField(auto_now=True)
    _features = models.TextField(db_column='features', blank=True)

    @property
    def features(self):
        return self._features.split(',')

    @features.setter
    def features(self, value):
        self._features = ','.join(value)

    @cached_property
    def model(self):
        if self.type == self.TYPE_KERAS:
            return self.retrieve_keras_model()

    def __clear_model_cache(self):
        try:
            del self.__dict__['model']
        except KeyError:
            pass
