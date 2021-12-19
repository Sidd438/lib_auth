# Generated by Django 4.0 on 2021-12-18 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0010_alter_book_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Returned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.TextField(null=True)),
                ('book_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='merit',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='returns',
            field=models.IntegerField(default=0),
        ),
    ]