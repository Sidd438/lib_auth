# Generated by Django 4.0 on 2021-12-18 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0003_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='location',
            new_name='bits_id',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
    ]