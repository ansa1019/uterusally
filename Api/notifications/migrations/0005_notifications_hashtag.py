# Generated by Django 4.1.7 on 2024-07-18 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("userprofile", "0016_subscribehashtag"),
        ("notifications", "0004_notifications_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="notifications",
            name="hashtag",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userprofile.subscribehashtag",
            ),
        ),
    ]
