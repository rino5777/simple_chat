# Generated by Django 4.2.4 on 2024-06-07 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_room_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
