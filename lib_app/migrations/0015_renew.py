# Generated by Django 4.0 on 2021-12-19 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0014_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Renew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=30)),
                ('time', models.IntegerField()),
            ],
        ),
    ]
