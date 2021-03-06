# Generated by Django 4.0.3 on 2022-03-12 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tables.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=20)),
                ('publishers', models.CharField(max_length=50)),
                ('available_qty', models.IntegerField(default=1)),
                ('book_pic', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(default=tables.models.one_month)),
                ('current_status', models.CharField(choices=[('iss', 'issued'), ('ret', 'returned'), ('ren', 'renewed')], max_length=8)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateField(auto_now_add=True)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.BigIntegerField(max_length=10)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
                ('branch', models.CharField(choices=[('MH', 'MH'), ('CL', 'CL'), ('CH', 'CH'), ('IC', 'IC'), ('IT', 'IT'), ('CE', 'CE'), ('EC', 'EC'), ('FOD', 'FOD'), ('FOP', 'FOP')], max_length=3)),
                ('profile_pic', models.ImageField(upload_to='images/')),
                ('address', models.TextField(default='Address not given')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penalty', models.IntegerField()),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(default=tables.models.one_month)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
