from django.apps import AppConfig
from oanda.features import register_all_oanda_features


class OandaConfig(AppConfig):
    name = 'oanda'

    def ready(self):
        register_all_oanda_features()
