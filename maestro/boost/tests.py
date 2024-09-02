from django.test import TestCase
from django.utils import timezone
from .models import Boost, Player, PlayerBoost
from django.contrib.auth.models import User
from datetime import timedelta


class PlayerModelTests(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password')
        self.player = Player.objects.create(user=self.user)

        # Создаем тестовый буст
        self.boost = Boost.objects.create(type='speed', value=10, duration=timedelta(minutes=5))

        # Создаем тестовые очки
        self.player.add_points(100)

    def test_add_boost(self):
        # Добавляем буст игроку
        player_boost = self.player.add_boost(self.boost, duration=timedelta(minutes=10))

        # Проверяем, что буст был добавлен
        self.assertEqual(PlayerBoost.objects.count(), 1)
        self.assertEqual(player_boost.boost, self.boost)
        self.assertEqual(player_boost.player, self.player)
        self.assertEqual(player_boost.duration, timedelta(minutes=10))

    def test_add_points(self):
        # Начисляем очки
        self.player.add_points(50)

        # Проверяем, что очки обновились
        self.assertEqual(self.player.points, 150)

    def test_update_first_login_date(self):
        # Обновляем дату первого входа
        self.player.update_first_login_date()

        # Проверяем, что дата первого входа была установлена
        self.assertIsNotNone(self.player.first_login_date)
        self.assertEqual(self.player.first_login_date.date(), timezone.now().date())

    def test_player_boost_str(self):
        # Добавляем буст игроку
        player_boost = self.player.add_boost(self.boost, duration=timedelta(minutes=10))

        # Проверяем строковое представление
        self.assertEqual(str(player_boost), f"{self.player.user.username} - Speed Boost")

    def test_boost_str(self):
        # Проверяем строковое представление буста
        self.assertEqual(str(self.boost), "Speed Boost (Value: 10)")

