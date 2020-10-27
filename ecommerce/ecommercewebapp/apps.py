from django.apps import AppConfig


class EcommercewebappConfig(AppConfig):
    name = 'ecommercewebapp'
    def ready(self):
        import ecommercewebapp.signals
