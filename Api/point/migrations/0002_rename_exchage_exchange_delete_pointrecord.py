# Generated by Django 4.1.7 on 2023-08-29 08:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0006_alter_product_category_category_name'),
        ('point', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='exchage',
            new_name='exchange',
        ),
        migrations.DeleteModel(
            name='pointRecord',
        ),
    ]
