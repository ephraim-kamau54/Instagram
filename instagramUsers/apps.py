from django.apps import AppConfig


class InstagramusersConfig(AppConfig):
    name = 'instagramUsers'

    def ready(self):
        import instagramUsers.signals
