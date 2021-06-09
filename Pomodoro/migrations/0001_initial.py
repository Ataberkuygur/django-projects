# Generated by Django 3.2.4 on 2021-06-09 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pomodoro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Pomodoro Time', max_length=100)),
                ('minutes', models.PositiveIntegerField(default=25)),
                ('seconds', models.PositiveIntegerField(default=0)),
                ('rest_minutes', models.PositiveIntegerField(default=5)),
                ('rest_seconds', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
