# Generated by Django 4.1.7 on 2023-10-16 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_alter_texteditorpost_identity'),
    ]

    operations = [
        migrations.AddField(
            model_name='texteditorpost',
            name='is_official',
            field=models.BooleanField(default=False),
        ),
    ]
