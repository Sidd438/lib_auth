# Generated by Django 4.0 on 2022-01-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0005_alter_issue_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
