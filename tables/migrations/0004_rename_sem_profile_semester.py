# Generated by Django 4.0.3 on 2022-03-16 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0003_profile_sem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='sem',
            new_name='semester',
        ),
    ]