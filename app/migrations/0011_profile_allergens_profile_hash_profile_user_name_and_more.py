# Generated by Django 4.0.2 on 2022-02-20 11:08

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_profile_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='allergens',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(0, 'Gluten'), (1, 'Dairy'), (2, 'Eggs'), (3, 'Fish'), (4, 'Peanuts')], default='', max_length=9),
        ),
        migrations.AddField(
            model_name='profile',
            name='hash',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='diet',
            field=models.IntegerField(default=-1),
        ),
    ]