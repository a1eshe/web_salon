from django.apps import AppConfig


class SalonWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salon_web'

def ready(self):
    import salon_web.signals
