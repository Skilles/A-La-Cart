# Generated by Django 4.0.2 on 2022-02-20 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_profile_avatar_remove_profile_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='diet',
            field=models.CharField(default='', max_length=200),
        ),
    ]
