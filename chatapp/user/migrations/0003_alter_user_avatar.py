# Generated by Django 4.2.4 on 2024-06-06 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='static/media/avatar/no_image.png', null=True, upload_to='static/media/avatar/'),
        ),
    ]
