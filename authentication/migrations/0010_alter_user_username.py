# Generated by Django 3.2.8 on 2021-10-16 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20211016_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name="Nom d'utilisateur"),
        ),
    ]