# Generated by Django 3.2.12 on 2022-03-22 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
            ],
        ),
    ]
