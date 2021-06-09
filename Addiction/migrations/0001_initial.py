# Generated by Django 3.2.4 on 2021-06-09 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Addiction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('day', models.PositiveIntegerField(editable=False, null=True)),
                ('week', models.PositiveIntegerField(editable=False, null=True)),
                ('month', models.PositiveIntegerField(editable=False, null=True)),
            ],
        ),
    ]
