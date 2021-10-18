# Generated by Django 3.2.8 on 2021-10-13 17:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='staff',
            new_name='is_staff',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='superuser',
            new_name='is_superuser',
        ),
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
