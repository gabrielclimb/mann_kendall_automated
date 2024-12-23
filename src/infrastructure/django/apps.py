from django.apps import AppConfig


class MannKendallConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mann_kendall"
    verbose_name = "Mann Kendall Analysis"


class DjangoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.infrastructure.django"
    label = "django"
    verbose_name = "Mann Kendall Analysis"
