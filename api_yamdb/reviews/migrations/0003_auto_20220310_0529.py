# Generated by Django 2.2.16 on 2022-03-10 05:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220306_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(10, 'Value less or equal 10'), django.core.validators.MinValueValidator(1, 'Value more or equal 1')], verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(verbose_name='year of writing'),
        ),
    ]