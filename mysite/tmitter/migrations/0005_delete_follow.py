# Generated by Django 3.2 on 2021-05-24 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmitter', '0004_follow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]