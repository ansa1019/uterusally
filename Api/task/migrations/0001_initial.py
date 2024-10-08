# Generated by Django 4.1.7 on 2023-08-29 03:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('point', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('type', models.CharField(blank=True, choices=[('BEGGINER', 'beginner'), ('DAILY', 'daily'), ('EVENT', 'event')], default='', max_length=100, null=True)),
                ('progress', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('requirement', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='taskRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(blank=True, default=False, null=True)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.task')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='taskPorgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.task')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
