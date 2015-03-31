from django.apps import AppConfig

class PlaneConfig(AppConfig):
    name = 'plogs.planes'

    def ready(self):
        import plogs.planes.signals