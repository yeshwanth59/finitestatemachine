# Generated by Django 3.0.2 on 2020-11-24 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statemachine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=41)),
                ('mobileNo', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=20)),
                ('pwd', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='userstatemapping',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statemachine.User'),
        ),
    ]
