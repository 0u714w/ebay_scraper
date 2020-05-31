# Generated by Django 3.0.6 on 2020-05-31 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multiply', '0008_auto_20200531_0106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericfile',
            old_name='csv',
            new_name='selling',
        ),
        migrations.AddField(
            model_name='genericfile',
            name='sold',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='genericfile',
            name='file',
            field=models.FileField(upload_to='files/'),
        ),
    ]
