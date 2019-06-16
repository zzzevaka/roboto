import v20

from django.conf import settings


def get_oanda_api_client():
    return v20.Context(
        hostname=settings.OANDA_API_HOST,
        port=settings.OANDA_API_PORT,
        token=settings.OANDA_API_TOKEN
    )
