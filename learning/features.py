from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from django.utils.module_loading import import_module
from django.conf import settings


class LearningFeature(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def load(self, start_time=None, end_time=None):
        pass

    def __str__(self):
        return 'LearningFeature: {}'.format(self.name)

    def __repr__(self):
        return str(self)


class LearningFeatureStore(object):

    stores = {}

    def __init__(self):
        self.__features = OrderedDict()

    @property
    def features(self):
        return self.__features

    def register(self, feature):
        if not isinstance(feature, LearningFeature):
            raise TypeError('feature must be a subclass of LearningFeature')
        self.__features[feature.name] = feature

    def register_all(self):
        raise NotImplementedError

    def merge(self, another_store):
        new_store = self.__class__()
        new_store.__features.update(self.__features)
        new_store.__features.update(another_store.__features)
        return new_store

    @classmethod
    def get_all_features_store(cls):
        store = LearningFeatureStore()
        for subclass in cls.__subclasses__():
            tmp_store = subclass()
            try:
                tmp_store.register_all()
                store = store.merge(tmp_store)
            except NotImplementedError:
                continue
        return store

    @classmethod
    def register_store(cls, store_class):
        cls.stores[store_class.name] = store_class


def discover_features():
    for store_class in settings.FEATURE_STORES:
        import_module(store_class)


def get_features(filter_func=lambda x: True):
    store = LearningFeatureStore.get_all_features_store()
    return [f for f in store.features if filter_func(f)]


discover_features()
