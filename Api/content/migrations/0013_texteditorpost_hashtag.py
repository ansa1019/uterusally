# Generated by Django 4.1.7 on 2023-11-21 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_remove_hashtag_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='texteditorpost',
            name='hashtag',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
