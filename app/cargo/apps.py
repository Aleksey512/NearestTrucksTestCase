from django.apps import AppConfig
import pandas as pd
from pathlib import Path

from django.db import IntegrityError

class CargoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cargo'
