from django.test import TestCase
from datetime import datetime
from .models import Player, Level, Prize, PlayerLevel, LevelPrize


from django.urls import reverse


class PlayerLevelTestCase(TestCase):

    def setUp(self):
        # Тестовые данные
        self.player = Player.objects.create(player_id='test_player')
        self.level = Level.objects.create(title='test_level')
        self.prize = Prize.objects.create(title='test_prize')
        self.completed_date = datetime.strptime('2024-09-01', '%Y-%m-%d').date()
        self.player_level = PlayerLevel.objects.create(
            player=self.player,
            level=self.level,
            completed=self.completed_date,
            is_completed=True
        )

    def test_award_prize(self):
        # Присваиваем приз
        self.player_level.award_prize(self.prize)

        # Проверка на добавление приза
        level_prizes = LevelPrize.objects.filter(level=self.level, prize=self.prize)
        self.assertEqual(level_prizes.count(), 1)

        # Проверка даты
        self.assertEqual(level_prizes.first().received, self.completed_date)

    def test_award_prize_not_completed(self):
        # Создание нового PlayerLevel с непроизведенным уровнем
        incomplete_player_level = PlayerLevel.objects.create(
            player=self.player,
            level=self.level,
            completed=self.completed_date,
            is_completed=False
        )

        # Проверка на исключения
        with self.assertRaises(ValueError):
            incomplete_player_level.award_prize(self.prize)


class ExportPlayerLevelsToCSV(TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.player = Player.objects.create(player_id='test_player')
        self.level = Level.objects.create(title='test_level')
        self.prize = Prize.objects.create(title='test_prize')
        self.player_level = PlayerLevel.objects.create(
            player=self.player,
            level=self.level,
            completed='2024-09-01',
            is_completed=True
        )
        LevelPrize.objects.create(level=self.level, prize=self.prize, received='2024-09-01')

    def test_csv_export(self):
        url = reverse('export_player_levels_to_csv')
        response = self.client.get(url)

        # Проверка на статус
        self.assertEqual(response.status_code, 200)

        # Проверка типа контента
        self.assertEqual(response['Content-Type'], 'text/csv')

        # Проверка заголовка
        self.assertIn('attachment; filename="player_levels.csv"', response['Content-Disposition'])

        # Проверка содержимого
        content = response.content.decode('utf-8')
        content = content.replace('\r', '')

        expected_header = 'Player ID,Level Title,Is Completed,Prize Title\n'
        self.assertTrue(content.startswith(expected_header))


