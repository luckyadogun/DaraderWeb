# Generated by Django 2.2.10 on 2020-04-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200309_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='admin'),
        ),
    ]