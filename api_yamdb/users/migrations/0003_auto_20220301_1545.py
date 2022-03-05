# Generated by Django 2.2.16 on 2022-03-01 12:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220301_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, unique=True, verbose_name='код подтверждения'),
        ),
    ]