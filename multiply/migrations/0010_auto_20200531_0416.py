# Generated by Django 3.0.6 on 2020-05-31 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multiply', '0009_auto_20200531_0401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericfile',
            old_name='selling',
            new_name='csv',
        ),
        migrations.RemoveField(
            model_name='genericfile',
            name='sold',
        ),
    ]
