from django.apps import AppConfig

class BuildLogConfig(AppConfig):
    name = 'plogs.buildlogs'

    def ready(self):
        import plogs.buildlogs.signals