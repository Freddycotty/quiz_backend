# Generated by Django 3.2.13 on 2022-05-06 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0024_alter_preguntas_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntas',
            name='photo',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]
