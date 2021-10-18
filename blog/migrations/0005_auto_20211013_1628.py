# Generated by Django 3.2.8 on 2021-10-13 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_ticket_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Critique', 'verbose_name_plural': 'Critiques'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
        migrations.AlterModelOptions(
            name='userfollows',
            options={'verbose_name': 'Utilisateur suivi', 'verbose_name_plural': 'Utilisateurs suivis'},
        ),
        migrations.AlterField(
            model_name='ticket',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]