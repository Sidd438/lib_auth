# Generated by Django 4.0 on 2021-12-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0017_alter_book_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='location',
            field=models.CharField(default='ask the librarian', max_length=100),
        ),
    ]