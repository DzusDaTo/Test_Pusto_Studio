from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class Boost(models.Model):
    BOOST_TYPE_CHOICES = [
        ('speed', 'Speed Boost'),
        ('strength', 'Strength Boost'),
        ('shield', 'Shield Boost'),
    ]

    type = models.CharField(max_length=50, choices=BOOST_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    value = models.PositiveIntegerField(default=0)  # Значение буста, например, его сила или количество
    duration = models.DurationField(blank=True, null=True)  # Длительность действия буста

    def __str__(self):
        return f"{self.get_type_display()} (Value: {self.value})"


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    points = models.PositiveIntegerField(default=0)  # Очки игрока
    first_login_date = models.DateTimeField(null=True, blank=True)  # Время первого входа игрока
    boosts = models.ManyToManyField(Boost, through='PlayerBoost', related_name='players')

    def __str__(self):
        return self.user.username

    def add_boost(self, boost, duration=None):
        """Метод для начисления буста игроку"""
        player_boost = PlayerBoost.objects.create(player=self, boost=boost, duration=duration)
        return player_boost

    def add_points(self, points):
        """Метод для начисления очков игроку"""
        self.points += points
        self.save()

    def update_first_login_date(self):
        """Метод для обновления времени первого входа"""
        if not self.first_login_date:
            self.first_login_date = timezone.now()
            self.save()


class PlayerBoost(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    boost = models.ForeignKey(Boost, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(blank=True, null=True)  # Длительность действия буста для конкретного игрока

    def __str__(self):
        return f"{self.player.user.username} - {self.boost.get_type_display()}"

