# Generated by Django 4.1.3 on 2022-12-21 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
