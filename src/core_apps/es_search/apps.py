from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EsSearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.es_search"
    verbose_name = _("Elastic Search")
