# Generated by Django 4.0 on 2021-12-19 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0018_book_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='issues',
            field=models.IntegerField(default=0),
        ),
    ]
