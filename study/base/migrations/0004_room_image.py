# Generated by Django 4.1.5 on 2023-01-16 08:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=None),
            preserve_default=False,
        ),
    ]
