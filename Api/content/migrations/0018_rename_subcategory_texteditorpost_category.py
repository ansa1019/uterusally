# Generated by Django 4.1.7 on 2024-04-24 14:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0017_remove_texteditorpost_category_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="texteditorpost",
            old_name="subcategory",
            new_name="category",
        ),
    ]
