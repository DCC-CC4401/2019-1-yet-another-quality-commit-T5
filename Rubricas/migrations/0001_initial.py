# Generated by Django 2.2.1 on 2019-05-16 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rubrica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('score', models.CharField(max_length=50)),
                ('aspects', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
    ]
