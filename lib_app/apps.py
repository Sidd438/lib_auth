from django.apps import AppConfig


class LibAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lib_app'
    def ready(self):
        import lib_app.signals