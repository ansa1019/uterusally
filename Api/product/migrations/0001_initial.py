# Generated by Django 4.1.7 on 2023-08-29 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=100)),
                ('amount', models.PositiveIntegerField()),
                ('exchaged', models.PositiveIntegerField()),
                ('product_point', models.IntegerField()),
                ('product_image', models.ImageField(upload_to='product_image')),
                ('product_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='product_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_image', models.ImageField(upload_to='category_image')),
                ('category_description', models.CharField(max_length=100)),
                ('category_product', models.ManyToManyField(related_name='product_category', to='product.product')),
            ],
        ),
    ]
