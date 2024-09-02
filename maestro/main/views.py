import csv
from django.http import HttpResponse
from .models import PlayerLevel, LevelPrize


def export_player_levels_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="player_levels.csv"'
    writer = csv.writer(response)
    writer.writerow(['Player ID', 'Level Title', 'Is Completed', 'Prize Title'])

    # Оптимизация
    for player_level in PlayerLevel.objects.select_related('player', 'level').prefetch_related('level__levelprize_set'):
        player_id = player_level.player.player_id
        level_title = player_level.level.title
        is_completed = player_level.is_completed

        # Поиск приза для уровня
        prizes = LevelPrize.objects.filter(level=player_level.level)
        prize_titles = [prize.prize.title for prize in prizes]

        for prize_title in prize_titles:
            writer.writerow([player_id, level_title, is_completed, prize_title])

    return response
