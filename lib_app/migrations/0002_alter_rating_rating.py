# Generated by Django 4.0 on 2021-12-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]