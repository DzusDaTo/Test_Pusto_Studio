from django.contrib import admin
from django.urls import path

from main.views import export_player_levels_to_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('export_player_levels/', export_player_levels_to_csv, name='export_player_levels_to_csv'),
]
