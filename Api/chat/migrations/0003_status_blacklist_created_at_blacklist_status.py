# Generated by Django 4.1.7 on 2024-05-08 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_blacklist"),
    ]

    operations = [
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="blacklist",
            name="created_at",
            field=models.DateTimeField(auto_created=True, auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="blacklist",
            name="status",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                to="chat.status",
            ),
        ),
    ]
