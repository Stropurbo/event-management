# Generated by Django 5.1.6 on 2025-03-06 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_participant_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('UPCOMING', 'upcoming'), ('COMPLETED', 'Completed')], db_index=True, default='UPCOMING', max_length=30),
        ),
        migrations.AlterField(
            model_name='participant',
            name='event',
            field=models.ManyToManyField(related_name='participants', to='tasks.event'),
        ),
    ]
