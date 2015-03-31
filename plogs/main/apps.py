from django.apps import AppConfig

class MainAppConfig(AppConfig):
    name = 'plogs.main'

    def ready(self):
        import plogs.main.signals