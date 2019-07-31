from django.conf import settings


def common_settings(context):
    return {
        'TEST_TITLE': settings.TEST_TITLE,
    }
