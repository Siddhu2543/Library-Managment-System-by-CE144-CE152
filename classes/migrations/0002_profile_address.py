# Generated by Django 4.0.3 on 2022-03-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(default='Address not given'),
        ),
    ]
