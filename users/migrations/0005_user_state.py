# Generated by Django 2.2.10 on 2020-04-30 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
        ('users', '0004_auto_20200409_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='properties.State'),
        ),
    ]