# Generated by Django 2.2.10 on 2020-07-09 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_auto_20200708_0949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name_plural': 'FAQs'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name_plural': 'Rooms'},
        ),
    ]
