# Generated by Django 4.1.7 on 2024-05-08 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0019_texteditorpost_reading_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='texteditorpost',
            name='click_count',
            field=models.IntegerField(default=0),
        ),
    ]
