# Generated by Django 3.0.8 on 2020-12-26 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentportal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='show_to_students',
            field=models.BooleanField(default=True),
        ),
    ]
