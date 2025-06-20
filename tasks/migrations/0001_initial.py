# Generated by Django 5.1.6 on 2025-05-28 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(db_index=True)),
                ('time', models.TimeField(auto_now=True)),
                ('location', models.CharField(max_length=250)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('status', models.CharField(choices=[('UPCOMING', 'upcoming'), ('COMPLETED', 'Completed')], db_index=True, default='UPCOMING', max_length=30)),
                ('asset', models.ImageField(blank=True, null=True, upload_to='event_asset')),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tasks.category')),
            ],
        ),
    ]
