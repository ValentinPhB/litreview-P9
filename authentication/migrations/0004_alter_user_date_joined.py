# Generated by Django 3.2.8 on 2021-10-13 17:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 17, 56, 14, 320409, tzinfo=utc)),
        ),
    ]