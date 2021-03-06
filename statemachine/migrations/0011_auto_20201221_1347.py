# Generated by Django 3.0.2 on 2020-12-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statemachine', '0010_auto_20201221_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default=False, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='upload/images'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
