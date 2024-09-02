# Generated by Django 5.1 on 2024-09-02 12:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('speed', 'Speed Boost'), ('strength', 'Strength Boost'), ('shield', 'Shield Boost')], max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('value', models.PositiveIntegerField(default=0)),
                ('duration', models.DurationField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField(default=0)),
                ('first_login_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerBoost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('boost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boost.boost')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boost.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='boosts',
            field=models.ManyToManyField(related_name='players', through='boost.PlayerBoost', to='boost.boost'),
        ),
    ]
