# Generated by Django 4.1.7 on 2023-09-21 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_profile_page_music'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodyprofile',
            name='created_at',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, null=True),
        ),
    ]
