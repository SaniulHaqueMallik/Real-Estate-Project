# Generated by Django 5.0.4 on 2024-05-06 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='photo6',
            field=models.ImageField(blank=True, upload_to='photo/%Y/%m/%d'),
        ),
    ]
