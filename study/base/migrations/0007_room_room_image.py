# Generated by Django 4.1.5 on 2023-01-17 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_room_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]