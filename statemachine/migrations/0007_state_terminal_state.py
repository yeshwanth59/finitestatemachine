# Generated by Django 3.0.2 on 2020-12-11 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statemachine', '0006_userstate_option_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='terminal_state',
            field=models.BooleanField(default=False),
        ),
    ]
