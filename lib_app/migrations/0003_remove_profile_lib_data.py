# Generated by Django 4.0 on 2022-01-09 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='lib_data',
        ),
    ]