from tensorflow.keras.models import load_model
from tempfile import NamedTemporaryFile


class KerasModelMixin(object):

    def save_keras_model(self, keras_model):
        with NamedTemporaryFile() as f:
            keras_model.save(f.name)
            self.file.save('{}.m5'.format(self.name), f)

    def retrieve_keras_model(self):
        with self.file.open() as f:
            return load_model(f)
